from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import PaperGenerateSerializer, GeneratedPaperSerializer
from questions.models import Subject, Chapter, Topic, Subtopic, Question
from .models import GeneratedPaper
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
import random

# Create your views here.

class PaperGenerateAPIView(APIView):
    @swagger_auto_schema(
        request_body=PaperGenerateSerializer,
        responses={
            200: openapi.Response(
                description="Generated question paper.",
                examples={
                    "application/json": {
                        "questions": [
                            {
                                "id": 1,
                                "text": "Sample question",
                                "question_type": "mcq",
                                "difficulty": "easy",
                                "option_a": "Option A",
                                "option_b": "Option B",
                                "option_c": "Option C",
                                "option_d": "Option D",
                                "correct_answer": "a",
                                "explanation": "Explanation text."
                            }
                        ]
                    }
                }
            )
        },
        operation_description="Generate a question paper based on subject/chapter/topic/subtopic, question type, difficulty, and number of questions."
    )
    def post(self, request):
        serializer = PaperGenerateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        mode = data['mode']
        values = data['value']
        question_type = data['question_type']
        difficulty = data['difficulty']
        num_questions = data['num_questions']

        queryset = Question.objects.all()
        if mode == 'subject':
            queryset = queryset.filter(subtopic__topic__chapter__subject__name__in=values)
        elif mode == 'chapter':
            queryset = queryset.filter(subtopic__topic__chapter__name__in=values)
        elif mode == 'topic':
            queryset = queryset.filter(subtopic__topic__name__in=values)
        elif mode == 'subtopic':
            queryset = queryset.filter(subtopic__name__in=values)

        if question_type != 'mixed':
            queryset = queryset.filter(question_type=question_type)
        if difficulty != 'mixed':
            queryset = queryset.filter(difficulty=difficulty)

        questions = list(queryset)
        if len(questions) > num_questions:
            questions = random.sample(questions, num_questions)
        result = [
            {
                'id': q.id,
                'text': q.text,
                'question_type': q.question_type,
                'difficulty': q.difficulty,
                'option_a': q.option_a,
                'option_b': q.option_b,
                'option_c': q.option_c,
                'option_d': q.option_d,
                'correct_answer': q.correct_answer,
                'explanation': q.explanation
            } for q in questions
        ]
        # Save generated paper for user if authenticated
        if request.user.is_authenticated:
            paper = GeneratedPaper.objects.create(user=request.user)
            paper.questions.set([q.id for q in questions])
            paper.save()
        return Response({'questions': result})

class UserGeneratedPaperListAPIView(generics.ListAPIView):
    serializer_class = GeneratedPaperSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GeneratedPaper.objects.filter(user=self.request.user).order_by('-created_at')
