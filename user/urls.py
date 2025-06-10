from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .views import LoginAPIView, RegisterAPIView, UserPreferenceAPIView, UserMeAPIView, UserPreferenceDetailAPIView, UserListWithPreferencesAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('me/', UserMeAPIView.as_view(), name='user_me'),
    path('preferences/', UserPreferenceAPIView.as_view(), name='user_preferences'),
    path('preferences/<int:pk>/', UserPreferenceDetailAPIView.as_view(), name='user_preference_detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('all/', UserListWithPreferencesAPIView.as_view(), name='user_list_with_preferences'),
]
