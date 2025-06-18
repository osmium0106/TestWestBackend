from django.urls import path
from .views import PaperGenerateAPIView, UserGeneratedPaperListAPIView

urlpatterns = [
    path('generate/', PaperGenerateAPIView.as_view(), name='paper_generate'),
    path('my-papers/', UserGeneratedPaperListAPIView.as_view(), name='user_generated_papers'),
]
