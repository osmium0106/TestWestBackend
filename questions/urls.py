from rest_framework.routers import DefaultRouter
from .views import (
    GradeViewSet, SubjectViewSet, ChapterViewSet, TopicViewSet, SubtopicViewSet, QuestionViewSet
)
from django.http import HttpResponse
from django.urls import path
from openpyxl import Workbook
import os

router = DefaultRouter()
router.register(r'grades', GradeViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'chapters', ChapterViewSet)
router.register(r'topics', TopicViewSet)
router.register(r'subtopics', SubtopicViewSet)
router.register(r'questions', QuestionViewSet)

def download_template(request):
    # Create an Excel workbook in memory
    wb = Workbook()
    ws = wb.active
    ws.title = "Questions Template"
    headers = ["text", "subtopic_name", "question_type", "difficulty", "option_a", "option_b", "option_c", "option_d", "correct_answer", "explanation"]
    ws.append(headers)
    ws.append(["What is the capital of France?", "Definition of a Set", "mcq", "easy", "Paris", "London", "Berlin", "Rome", "a", "Paris is the capital of France."])
    ws.append(["Which of the following are prime numbers?", "Definition of a Set", "msq", "medium", "2", "3", "4", "5", "a,b,d", "2, 3, and 5 are prime numbers."])
    ws.append(["What is 2+2?", "Definition of a Set", "short", "easy", "", "", "", "", "", "The answer is 4."])
    ws.append(["Describe the process of photosynthesis.", "Definition of a Set", "long", "medium", "", "", "", "", "", "Plants convert sunlight into energy."])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=sample_questions_template.xlsx'
    wb.save(response)
    return response

urlpatterns = router.urls + [
    path('download-template/', download_template, name='download_questions_template'),
]
