from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .views import LoginAPIView, RegisterAPIView, UserPreferenceAPIView, UserMeAPIView, UserPreferenceDetailAPIView, UserListWithPreferencesAPIView, UserGradeUpdateAPIView, GradeHierarchyAPIView, AddUserAPIView, SuperAdminListCreateAPIView, SchoolAdminListCreateAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('me/', UserMeAPIView.as_view(), name='user_me'),
    path('preferences/', UserPreferenceAPIView.as_view(), name='user_preferences'),
    path('preferences/<int:pk>/', UserPreferenceDetailAPIView.as_view(), name='user_preference_detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('all/', UserListWithPreferencesAPIView.as_view(), name='user_list_with_preferences'),
    path('grade/', UserGradeUpdateAPIView.as_view(), name='user_grade_update'),
    path('grade-hierarchy/', GradeHierarchyAPIView.as_view(), name='user_grade_hierarchy'),
    path('add-user/', AddUserAPIView.as_view(), name='add_user'),
    path('superadmins/', SuperAdminListCreateAPIView.as_view(), name='superadmin-list-create'),
    path('school-admins/', SchoolAdminListCreateAPIView.as_view(), name='schooladmin-list-create'),
]
