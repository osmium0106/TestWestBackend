from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('superadmin-dashboard/', views.superadmin_dashboard, name='superadmin_dashboard'),
    path('school-dashboard/', views.school_dashboard, name='school_dashboard'),
    path('generate-paper/', views.generate_paper, name='generate_paper'),
    path('my-papers/', views.my_papers, name='my_papers'),
]
