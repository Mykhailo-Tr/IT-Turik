from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q

from school_system.decorators import teacher_required, student_required
from accounts.models import User, UserProfile
from accounts.forms import StudentSignUpForm, TeacherSignUpForm, ParentSignUpForm, UserUpdateForm, UserProfileUpdateForm



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

    query = request.GET.get('q')
    if query:
        accounts = accounts.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )

    accounts_count = accounts.count()
    context = {
        'page': 'dashboard',
        'accounts': accounts,
        'accounts_count': accounts_count,
    }
    return render(request, 'dashboard/accounts.html', context)


@login_required(login_url='login')
def profile_view(request, user_id=None):
    user = User.objects.get(id=user_id)
    profile = UserProfile.objects.get(user=user)
    context = {
        'page': 'dashboard',
        'user': user,
        'profile': profile,
    }
    return render(request, 'accounts/profile.html', context)


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
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, f'{role.capitalize()} успішно створено.')
            return redirect('dashboard_accounts')
    
    context = {
        'page': 'dashboard',
        'form': form_class(),
        'role': role,
    }
    return render(request, 'dashboard/forms/create_user.html', context)


@teacher_required(login_url='login')
def delete_account_view(request, user_id=None):
    if user_id:
        user = User.objects.get(id=user_id)
    else:
        user = request.user
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Обліковий запис успішно видалено.')
        return redirect('dashboard_accounts')
    
    context = {
        'user': user,
    }
    return render(request, 'accounts/forms/delete_account.html', context)
    

@teacher_required(login_url='login')
def edit_account_view(request, user_id=None):
    if user_id:
        user = User.objects.get(id=user_id)
    else:
        messages.error(request, 'Невірний запит.')
        return redirect('dashboard_accounts')
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been updated.')
            return redirect('dashboard_accounts')
    else:
        form = UserUpdateForm(instance=user)
        
    context = {
        'page': 'edit_account',
        'form': form,
    }
    return render(request, 'accounts/forms/edit_account.html', context)


@teacher_required(login_url='login')
def edit_profile_view(request, user_id=None):
    if user_id:
        user = User.objects.get(id=user_id)
    else:
        messages.error(request, 'Невірний запит.')
        return redirect('dashboard_accounts')
        
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('dashboard_accounts')
    else:
        form = UserProfileUpdateForm(instance=user.profile)
        
    context = {
        'page': 'edit_profile',
        'form': form,
    }
    return render(request, 'accounts/forms/edit_profile.html', context)
