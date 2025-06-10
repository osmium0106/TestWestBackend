from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg import openapi
from rest_framework import generics, permissions
from .serializers import RegisterSerializer, UserPreferenceSerializer, UserSerializer
from .models import UserPreference
from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveUpdateAPIView

User = get_user_model()

# Create your views here.

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(default="admin")
    password = serializers.CharField(write_only=True, style={'input_type': 'password'}, default="1234")

class LoginAPIView(APIView):
    authentication_classes = []  # Disable authentication for login
    permission_classes = []
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="Login successful. Use the access token below as 'Bearer <token>' in the Authorize box.",
                examples={
                    "application/json": {
                        "refresh": "<refresh_token>",
                        "access": "<access_token>",
                        "message": "Login successful"
                    }
                }
            )
        },
        operation_description="Login and receive JWT tokens. Copy the 'access' token and paste it as 'Bearer <token>' in the Authorize box above."
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                response = Response({
                    'refresh': str(refresh),
                    'access': access_token,
                    'message': 'Login successful'
                }, status=status.HTTP_200_OK)
                response['Authorization'] = f'Bearer {access_token}'
                return response
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(operation_description="Register a new user (user or admin)", tags=["User"], responses={201: UserSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class UserPreferenceAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=UserPreferenceSerializer,
        operation_description="Set or update user preferences (grade, subjects, chapters, topics)",
        tags=["UserPreferences"]
    )
    def post(self, request):
        # Set or update preferences
        pref, _ = UserPreference.objects.get_or_create(user=request.user)
        serializer = UserPreferenceSerializer(pref, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(operation_description="Get user preferences", tags=["User"])
    def get(self, request):
        pref, _ = UserPreference.objects.get_or_create(user=request.user)
        serializer = UserPreferenceSerializer(pref)
        return Response(serializer.data)

class UserMeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(operation_description="Get current user info (with role and preferences)", tags=["User"])
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class UserPreferenceDetailAPIView(RetrieveUpdateAPIView):
    queryset = UserPreference.objects.all()
    serializer_class = UserPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_serializer_context(self):
        from questions.models import Grade, Subject, Chapter, Topic
        return {
            **super().get_serializer_context(),
            'grade_choices': [(g.name, g.name) for g in Grade.objects.all()],
            'subject_choices': [(s.name, s.name) for s in Subject.objects.all()],
            'chapter_choices': [(c.name, c.name) for c in Chapter.objects.all()],
            'topic_choices': [(t.name, t.name) for t in Topic.objects.all()],
        }

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(UserPreference, pk=pk)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def get_request_body_schema(self):
        context = self.get_serializer_context()
        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'grade': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=[g[0] for g in context['grade_choices']],
                    description='Select from available grades.'
                ),
                'subjects': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_STRING, enum=[s[0] for s in context['subject_choices']]),
                    description='Select from available subjects.'
                ),
                'chapters': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_STRING, enum=[c[0] for c in context['chapter_choices']]),
                    description='Select from available chapters.'
                ),
                'topics': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_STRING, enum=[t[0] for t in context['topic_choices']]),
                    description='Select from available topics.'
                ),
            },
            required=['grade', 'subjects', 'chapters', 'topics']
        )

    @swagger_auto_schema(
        request_body=None,
        operation_description="Set or update user preferences (grade, subjects, chapters, topics) with dropdowns. Dropdowns will appear if choices are available.",
        tags=["User"]
    )
    def post(self, request, *args, **kwargs):
        # For explicit POST to create preference for a user by pk
        pk = self.kwargs.get('pk')
        user_pref, created = UserPreference.objects.get_or_create(pk=pk)
        serializer = self.get_serializer(user_pref, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201 if created else 200)
        return Response(serializer.errors, status=400)

class UserListWithPreferencesAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]
    @swagger_auto_schema(
        operation_description="Get all users with their preferences (admin only)",
        tags=["User"]
    )
    def get(self, request):
        users = User.objects.all()
        data = UserSerializer(users, many=True).data
        return Response(data)
