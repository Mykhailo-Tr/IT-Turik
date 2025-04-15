from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from .models import User
from .forms import StudentSignUpForm, TeacherSignUpForm, ParentSignUpForm, UserUpdateForm, UserProfileUpdateForm
from .forms import LoginForm
from django.urls import reverse_lazy
from school_system.decorators import teacher_required, student_required



def main_page(request):
    return render(request, 'home_page.html')


class UserLoginView(LoginView):
    template_name = 'accounts/login_form.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        kwargs['page'] = 'login'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect('home')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid email or password.')
        return redirect('login')


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
def account_view(request):
    context = {
        'page': 'account',
    }
    return render(request, 'accounts/account.html', context)


@login_required(login_url='login')
def profile_view(request):
    context = {
        'page': 'profile',
        'profile': request.user.profile,
    }
    return render(request, 'accounts/profile.html', context)


@login_required(login_url='login')
def edit_account_view(request):      
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been updated.')
            return redirect('account')
    else:
        form = UserUpdateForm(instance=request.user)
        
    context = {
        'page': 'edit_account',
        'form': form,
    }
    return render(request, 'accounts/edit_account_form.html', context)


@login_required(login_url='login')
def edit_profile_view(request):
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('account')
    else:
        form = UserProfileUpdateForm(instance=request.user.profile)
        
    context = {
        'page': 'edit_profile',
        'form': form,
    }
    return render(request, 'accounts/edit_profile_form.html', context)

