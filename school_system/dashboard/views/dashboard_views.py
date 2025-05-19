from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy, reverse
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
    else:
        form = form_class()  # GET запит → пуста форма

    context = {
        'page': 'dashboard',
        'form': form,  # ✅ передається актуальна форма з помилками, якщо є
        'role': role,
    }
    return render(request, 'dashboard/forms/create_user.html', context)


