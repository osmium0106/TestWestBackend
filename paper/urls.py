from django.urls import path
from .views import PaperGenerateAPIView

urlpatterns = [
    path('generate/', PaperGenerateAPIView.as_view(), name='paper_generate'),
]
