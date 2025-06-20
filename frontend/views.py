from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from user.models import CustomUser
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect
from django import forms

User = get_user_model()

class CustomLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

@login_required
def dashboard(request):
    return render(request, 'frontend/dashboard.html')

@login_required
def superadmin_dashboard(request):
    if not request.user.is_authenticated or request.user.role != 'superadmin':
        return redirect('login')
    if request.method == 'POST':
        school_name = request.POST.get('school_name')
        max_users = int(request.POST.get('max_users'))
        admin_username = request.POST.get('admin_username')
        admin_email = request.POST.get('admin_email')
        admin_password = request.POST.get('admin_password')
        # Create school admin
        admin_user = User.objects.create_user(
            username=admin_username,
            email=admin_email,
            password=admin_password,
            role='school_admin',
            max_sub_users=max_users
        )
        admin_user.save()
        admin_user.school_name = school_name  # Optionally store school name
        admin_user.save()
    schools = User.objects.filter(role='school_admin')
    return render(request, 'frontend/superadmin_dashboard.html', {'schools': schools})

@login_required
def school_dashboard(request):
    if not request.user.is_authenticated or request.user.role != 'school_admin':
        return redirect('login')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Enforce max_sub_users
        if request.user.sub_users.count() < request.user.max_sub_users:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role='user',
                parent=request.user
            )
            user.save()
        else:
            return render(request, 'frontend/school_dashboard.html', {'users': request.user.sub_users.all(), 'error': 'Max users limit reached.'})
    users = request.user.sub_users.all()
    return render(request, 'frontend/school_dashboard.html', {'users': users})

@csrf_protect
def custom_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.role == 'superadmin':
                    return redirect('superadmin_dashboard')
                elif user.role == 'school_admin':
                    return redirect('school_dashboard')
                else:
                    return redirect('dashboard')
            else:
                return render(request, 'frontend/login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = CustomLoginForm()
    return render(request, 'frontend/login.html', {'form': form})

@login_required
def generate_paper(request):
    return render(request, 'frontend/generate_paper.html')

@login_required
def my_papers(request):
    return render(request, 'frontend/my_papers.html')