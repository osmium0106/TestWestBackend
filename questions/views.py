from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Grade, Subject, Chapter, Topic, Subtopic, Question
from .serializers import (
    GradeSerializer, SubjectSerializer, ChapterSerializer, TopicSerializer, SubtopicSerializer, QuestionSerializer
)
from django.db import transaction
from django.db.models import Q

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class SubtopicViewSet(viewsets.ModelViewSet):
    queryset = Subtopic.objects.all()
    serializer_class = SubtopicSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    @action(detail=False, methods=['post'], url_path='bulk_upload')
    def bulk_upload(self, request):
        """Bulk upload questions. Expects a list of question objects."""
        questions_data = request.data.get('questions', [])
        if not isinstance(questions_data, list):
            return Response({'error': 'questions must be a list'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=questions_data, many=True)
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = super().get_queryset()
        question_type = self.request.query_params.get('question_type')
        difficulty = self.request.query_params.get('difficulty')
        search = self.request.query_params.get('search')
        grade = self.request.query_params.get('grade')
        subject = self.request.query_params.get('subject')
        chapter = self.request.query_params.get('chapter')
        topic = self.request.query_params.get('topic')
        subtopic = self.request.query_params.get('subtopic')
        if question_type:
            queryset = queryset.filter(question_type=question_type)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        if search:
            queryset = queryset.filter(Q(text__icontains=search))
        if grade:
            queryset = queryset.filter(subtopic__topic__chapter__subject__grade__id=grade)
        if subject:
            queryset = queryset.filter(subtopic__topic__chapter__subject__id=subject)
        if chapter:
            queryset = queryset.filter(subtopic__topic__chapter__id=chapter)
        if topic:
            queryset = queryset.filter(subtopic__topic__id=topic)
        if subtopic:
            queryset = queryset.filter(subtopic__id=subtopic)
        return queryset
