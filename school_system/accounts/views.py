from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from .models import User
from .forms import StudentSignUpForm, TeacherSignUpForm, ParentSignUpForm
from .decorators import student_required, teacher_required


    

def main_page(request):
    return render(request, 'home_page.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('login')
    context = {
        'page': 'login',
    }
    return render(request, 'accounts/login_form.html', context)


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('home')


def register_view(request):
    context = {
        'page': 'register',
    }
    return render(request, 'accounts/register.html', context)


@login_required(login_url='login')
def delete_account_view(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('home')
    context = {
        'page': 'delete_account',
    }
    return render(request, 'accounts/delete_account_form.html', context)


class UserSignUpView(CreateView):
    model = User
    template_name = 'accounts/signup_form.html'
    form_class = None
    success_url = '/'
    redirect_authenticated_user = True
    
    
    def get_context_data(self, **kwargs):
        kwargs['page'] = 'register'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class StudentSignUpView(UserSignUpView):
    form_class = StudentSignUpForm

    def get_context_data(self, **kwargs):
        kwargs['role'] = 'student'
        return super().get_context_data(**kwargs)


class TeacherSignUpView(UserSignUpView):
    form_class = TeacherSignUpForm

    def get_context_data(self, **kwargs):
        kwargs['role'] = 'teacher'
        return super().get_context_data(**kwargs)
    

class ParentSignUpView(UserSignUpView):
    form_class = ParentSignUpForm

    def get_context_data(self, **kwargs):
        kwargs['role'] = 'parent'
        return super().get_context_data(**kwargs)


@login_required(login_url='login')
def dashboard_view(request):
    if request.user.role == 'teacher':
        return redirect('teacher_dashboard')
    else:
        return redirect('home')
    

@teacher_required(login_url='login')
def teacher_dashboard_view(request):
    accounts = User.objects.exclude(id=request.user.id)
    accounts_count = accounts.count()
    context = {
        'page': 'teacher_dashboard',
        'accounts': accounts,
        'accounts_count': accounts_count,
    }
    return render(request, 'accounts/teacher_dashboard.html', context)


@teacher_required(login_url='login')
def teacher_create_account_view(request, role):
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
            return redirect('teacher_dashboard')
    else:
        form = form_class()
        
    context = {
        'page': 'teacher_create_account',
        'form': form,
        'role': role,
    }
    return render(request, 'accounts/teacher_create_user_form.html', context)


@teacher_required(login_url='login')
def teacher_delete_account_view(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('teacher_dashboard')