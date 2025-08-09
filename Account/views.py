from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import StudentProfile
from .forms import CustomUserCreationForm, StudentProfileForm, CustomUserForm

User = get_user_model()

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Chào mừng {user.first_name or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng.')
    return render(request, 'account/login.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Tạo profile cho user
            StudentProfile.objects.create(user=user)
            messages.success(request, 'Đăng ký thành công! Bạn có thể đăng nhập ngay bây giờ.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'account/register.html', {'form': form})

@login_required
def dashboard_view(request):
    try:
        profile = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        profile = StudentProfile.objects.create(user=request.user)
    
    context = {
        'user': request.user,
        'profile': profile,
    }
    return render(request, 'account/dashboard.html', context)

@login_required
def profile_view(request):
    try:
        profile = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        profile = StudentProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        user_form = CustomUserForm(request.POST, request.FILES, instance=request.user)
        profile_form = StudentProfileForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Thông tin đã được cập nhật thành công!')
            return redirect('profile')
    else:
        user_form = CustomUserForm(instance=request.user)
        profile_form = StudentProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile,
    }
    return render(request, 'account/profile.html', context)

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Bạn đã đăng xuất thành công.')
    return redirect('login')
