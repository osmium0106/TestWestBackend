from django.contrib import admin
from .models import Grade, Subject, Chapter, Topic, Subtopic, Question
from django import forms
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
import csv
from io import TextIOWrapper

class QuestionBulkUploadForm(forms.Form):
    csv_file = forms.FileField(label="CSV file")

class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "subtopic", "question_type", "difficulty", "extra_field1", "extra_field2")
    list_filter = ("question_type", "difficulty", "extra_field1", "extra_field2", "subtopic__topic__chapter__subject__grade", "subtopic__topic__chapter__subject", "subtopic__topic__chapter", "subtopic__topic", "subtopic")
    search_fields = ("text", "extra_field1", "extra_field2")
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
                csv_file = TextIOWrapper(request.FILES['csv_file'].file, encoding='utf-8')
                reader = csv.DictReader(csv_file)
                created = 0
                for row in reader:
                    try:
                        subtopic_id = row.get('subtopic_id')
                        Question.objects.create(
                            text=row.get('text'),
                            subtopic_id=subtopic_id,
                            question_type=row.get('question_type'),
                            difficulty=row.get('difficulty'),
                            extra_field1=row.get('extra_field1'),
                            extra_field2=row.get('extra_field2'),
                        )
                        created += 1
                    except Exception as e:
                        messages.error(request, f"Error in row: {row} - {e}")
                messages.success(request, f"Successfully uploaded {created} questions.")
                return redirect("..")
        else:
            form = QuestionBulkUploadForm()
        return render(request, "admin/questions/bulk_upload.html", {"form": form})

admin.site.register(Grade)
admin.site.register(Subject)
admin.site.register(Chapter)
admin.site.register(Topic)
admin.site.register(Subtopic)
admin.site.register(Question, QuestionAdmin)
