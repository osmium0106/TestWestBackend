from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Grade, Subject, Chapter, Topic, Subtopic, Question
from .serializers import (
    GradeSerializer, SubjectSerializer, ChapterSerializer, TopicSerializer, SubtopicSerializer, QuestionSerializer
)
from django.db import transaction
from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

    @swagger_auto_schema(tags=["Grades"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Grades"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Grades"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Grades"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Grades"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Grades"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'preference') and user.role == 'user':
            pref = user.preference
            if pref.grade:
                return Grade.objects.filter(id=pref.grade.id)
        return super().get_queryset()

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    @swagger_auto_schema(tags=["Subjects"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Subjects"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Subjects"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Subjects"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Subjects"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Subjects"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'preference') and user.role == 'user':
            pref = user.preference
            if pref.subjects.exists():
                return Subject.objects.filter(id__in=pref.subjects.values_list('id', flat=True))
            elif pref.grade:
                return Subject.objects.filter(grade=pref.grade)
        return super().get_queryset()

class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

    @swagger_auto_schema(tags=["Chapters"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Chapters"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Chapters"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Chapters"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Chapters"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Chapters"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'preference') and user.role == 'user':
            pref = user.preference
            if pref.chapters.exists():
                return Chapter.objects.filter(id__in=pref.chapters.values_list('id', flat=True))
            elif pref.subjects.exists():
                return Chapter.objects.filter(subject__in=pref.subjects.all())
            elif pref.grade:
                return Chapter.objects.filter(subject__grade=pref.grade)
        return super().get_queryset()

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    @swagger_auto_schema(tags=["Topics"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Topics"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Topics"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Topics"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Topics"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Topics"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'preference') and user.role == 'user':
            pref = user.preference
            if pref.topics.exists():
                return Topic.objects.filter(id__in=pref.topics.values_list('id', flat=True))
            elif pref.chapters.exists():
                return Topic.objects.filter(chapter__in=pref.chapters.all())
            elif pref.subjects.exists():
                return Topic.objects.filter(chapter__subject__in=pref.subjects.all())
            elif pref.grade:
                return Topic.objects.filter(chapter__subject__grade=pref.grade)
        return super().get_queryset()

class SubtopicViewSet(viewsets.ModelViewSet):
    queryset = Subtopic.objects.all()
    serializer_class = SubtopicSerializer

    @swagger_auto_schema(tags=["Subtopics"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Subtopics"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Subtopics"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Subtopics"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Subtopics"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Subtopics"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'preference') and user.role == 'user':
            pref = user.preference
            if pref.topics.exists():
                return Subtopic.objects.filter(topic__in=pref.topics.all())
            elif pref.chapters.exists():
                return Subtopic.objects.filter(topic__chapter__in=pref.chapters.all())
            elif pref.subjects.exists():
                return Subtopic.objects.filter(topic__chapter__subject__in=pref.subjects.all())
            elif pref.grade:
                return Subtopic.objects.filter(topic__chapter__subject__grade=pref.grade)
        return super().get_queryset()

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    @swagger_auto_schema(tags=["Questions"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Questions"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Questions"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Questions"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Questions"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Questions"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Questions"])
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
        user = self.request.user
        queryset = super().get_queryset()
        if user.is_authenticated and hasattr(user, 'preference') and user.role == 'user':
            pref = user.preference
            if pref.topics.exists():
                queryset = queryset.filter(subtopic__topic__in=pref.topics.all())
            elif pref.chapters.exists():
                queryset = queryset.filter(subtopic__topic__chapter__in=pref.chapters.all())
            elif pref.subjects.exists():
                queryset = queryset.filter(subtopic__topic__chapter__subject__in=pref.subjects.all())
            elif pref.grade:
                queryset = queryset.filter(subtopic__topic__chapter__subject__grade=pref.grade)
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
