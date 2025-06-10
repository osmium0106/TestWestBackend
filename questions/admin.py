from django.contrib import admin
from .models import Grade, Subject, Chapter, Topic, Subtopic, Question
from django import forms
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
import csv
from io import TextIOWrapper
from django.utils.safestring import mark_safe
import chardet
import openpyxl

class QuestionBulkUploadForm(forms.Form):
    csv_file = forms.FileField(label="CSV file")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper_text = mark_safe('<a href="/api/questions/download-template/" target="_blank" class="button">Download Sample Template</a>')

    class Media:
        js = ('admin/questions/bulk_upload_dynamic.js',)

class QuestionAdminForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'

    class Media:
        js = ('admin/js/jquery.init.js', 'admin/questions/question_dynamic.js',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        qtype = self.initial.get('question_type', self.data.get('question_type'))
        if qtype in ['short', 'long']:
            self.fields['option_a'].widget = forms.HiddenInput()
            self.fields['option_b'].widget = forms.HiddenInput()
            self.fields['option_c'].widget = forms.HiddenInput()
            self.fields['option_d'].widget = forms.HiddenInput()
        else:
            self.fields['option_a'].widget = forms.TextInput()
            self.fields['option_b'].widget = forms.TextInput()
            self.fields['option_c'].widget = forms.TextInput()
            self.fields['option_d'].widget = forms.TextInput()

class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm
    list_display = ("text", "subtopic", "question_type", "difficulty", "option_a", "option_b", "option_c", "option_d", "correct_answer", "explanation")
    list_filter = ("question_type", "difficulty", "subtopic__topic__chapter__subject__grade", "subtopic__topic__chapter__subject", "subtopic__topic__chapter", "subtopic__topic", "subtopic")
    search_fields = ("text", "option_a", "option_b", "option_c", "option_d", "correct_answer", "explanation")
    change_list_template = "admin/questions/question_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('bulk_upload/', self.admin_site.admin_view(self.bulk_upload)),
        ]
        return custom_urls + urls

    def bulk_upload(self, request):
        if request.method == "POST":
            form = QuestionBulkUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file = request.FILES['csv_file']
                if file.name.endswith('.xlsx'):
                    wb = openpyxl.load_workbook(file)
                    ws = wb.active
                    rows = list(ws.iter_rows(values_only=True))
                    headers = [str(h).strip() for h in rows[0]]
                    created = 0
                    for row in rows[1:]:
                        row_dict = dict(zip(headers, row))
                        try:
                            subtopic_name = row_dict.get('subtopic_name')
                            subtopic = None
                            if subtopic_name:
                                try:
                                    subtopic = Subtopic.objects.get(name=subtopic_name)
                                except Subtopic.DoesNotExist:
                                    messages.error(request, f"Subtopic '{subtopic_name}' does not exist.")
                                    continue
                            Question.objects.create(
                                text=row_dict.get('text'),
                                subtopic=subtopic,
                                question_type=row_dict.get('question_type'),
                                difficulty=row_dict.get('difficulty'),
                                option_a=row_dict.get('option_a'),
                                option_b=row_dict.get('option_b'),
                                option_c=row_dict.get('option_c'),
                                option_d=row_dict.get('option_d'),
                                correct_answer=row_dict.get('correct_answer'),
                                explanation=row_dict.get('explanation'),
                            )
                            created += 1
                        except Exception as e:
                            messages.error(request, f"Error in row: {row_dict} - {e}")
                    messages.success(request, f"Successfully uploaded {created} questions.")
                    return redirect("..")
                else:
                    # CSV fallback (previous logic)
                    raw_data = file.read()
                    result = chardet.detect(raw_data)
                    encoding = result['encoding'] or 'utf-8'
                    file.seek(0)
                    csv_file = TextIOWrapper(file.file, encoding=encoding, errors='replace')
                    reader = csv.DictReader(csv_file)
                    created = 0
                    for row in reader:
                        try:
                            subtopic_name = row.get('subtopic_name')
                            subtopic = None
                            if subtopic_name:
                                try:
                                    subtopic = Subtopic.objects.get(name=subtopic_name)
                                except Subtopic.DoesNotExist:
                                    messages.error(request, f"Subtopic '{subtopic_name}' does not exist.")
                                    continue
                            Question.objects.create(
                                text=row.get('text'),
                                subtopic=subtopic,
                                question_type=row.get('question_type'),
                                difficulty=row.get('difficulty'),
                                option_a=row.get('option_a'),
                                option_b=row.get('option_b'),
                                option_c=row.get('option_c'),
                                option_d=row.get('option_d'),
                                correct_answer=row.get('correct_answer'),
                                explanation=row.get('explanation'),
                            )
                            created += 1
                        except Exception as e:
                            messages.error(request, f"Error in row: {row} - {e}")
                    messages.success(request, f"Successfully uploaded {created} questions.")
                    return redirect("..")
        else:
            form = QuestionBulkUploadForm()
        return render(request, "admin/questions/bulk_upload.html", {"form": form, "helper_text": form.helper_text})

admin.site.register(Grade)
admin.site.register(Subject)
admin.site.register(Chapter)
admin.site.register(Topic)
admin.site.register(Subtopic)
admin.site.register(Question, QuestionAdmin)

class TopicAdmin(admin.ModelAdmin):
    list_display = ("name", "chapter", "tag")
    list_filter = ("tag", "chapter")

admin.site.unregister(Topic)
admin.site.register(Topic, TopicAdmin)
