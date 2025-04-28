from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from school_system.decorators import teacher_required, student_required
from accounts.models import User, UserProfile
from accounts.forms import StudentSignUpForm, TeacherSignUpForm, ParentSignUpForm, UserUpdateForm, UserProfileUpdateForm
from django.urls import reverse_lazy



@login_required(login_url='login')
def dashboard_view(request):
    context = {
        'page': 'dashboard',
    }
    return render(request, 'dashboard/dashboard.html', context)    


@login_required(login_url='login')
def accounts_view(request):
    accounts = User.objects.exclude(id=request.user.id)

    if request.user.role in ['student', 'parent']:
        accounts = accounts.exclude(role='admin')
        
    accounts_count = accounts.count()
    context = {
        'page': 'dashboard_accounts',
        'accounts': accounts,
        'accounts_count': accounts_count,
    }
    return render(request, 'dashboard/accounts.html', context)


@login_required(login_url='login')
def profile_view(request, user_id=None):
    user = User.objects.get(id=user_id)
    profile = UserProfile.objects.get(user=user)
    context = {
        'page': 'profile',
        'user': user,
        'profile': profile,
    }
    return render(request, 'dashboard/profile.html', context)


@teacher_required(login_url='login')
def create_account_view(request, role):
    if role == 'student':
        form_class = StudentSignUpForm
    elif role == 'parent':
        form_class = ParentSignUpForm
    elif role == 'teacher':
        form_class = TeacherSignUpForm
    else:
        messages.error(request, 'Невідома роль.')
        return redirect('teacher_dashboard')
    
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, f'{role.capitalize()} успішно створено.')
            return redirect('teacher_accounts')
    
    context = {
        'page': 'teacher_create_account',
        'form': form_class(),
        'role': role,
    }
    return render(request, 'dashboard/create_user_form.html', context)


@teacher_required(login_url='login')
def delete_account_view(request, user_id=None):
    if user_id:
        user = User.objects.get(id=user_id)
    else:
        user = request.user
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Обліковий запис успішно видалено.')
        return redirect('teacher_accounts')
    
    context = {
        'page': 'delete_account',
        'user': user,
    }
    return render(request, 'accounts/delete_account_form.html', context)
    

@teacher_required(login_url='login')
def edit_account_view(request, user_id=None):
    if user_id:
        user = User.objects.get(id=user_id)
    else:
        messages.error(request, 'Невірний запит.')
        return redirect('teacher_accounts')
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been updated.')
            return redirect('teacher_accounts')
    else:
        form = UserUpdateForm(instance=user)
        
    context = {
        'page': 'edit_account',
        'form': form,
    }
    return render(request, 'accounts/edit_account_form.html', context)


@teacher_required(login_url='login')
def edit_profile_view(request, user_id=None):
    if user_id:
        user = User.objects.get(id=user_id)
    else:
        messages.error(request, 'Невірний запит.')
        return redirect('teacher_accounts')
        
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('teacher_accounts')
    else:
        form = UserProfileUpdateForm(instance=user.profile)
        
    context = {
        'page': 'edit_profile',
        'form': form,
    }
    return render(request, 'accounts/edit_profile_form.html', context)
