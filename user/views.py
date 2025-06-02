from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg import openapi

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
