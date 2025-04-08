from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from .models import User
from .forms import StudentSignUpForm, TeacherSignUpForm, ParentSignUpForm


    

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


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'accounts/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['role'] = 'student'
        kwargs['page'] = 'register'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'accounts/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['role'] = 'teacher'
        kwargs['page'] = 'register'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')
    

class ParentSignUpView(CreateView):
    model = User
    form_class = ParentSignUpForm
    template_name = 'accounts/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['role'] = 'parent'
        kwargs['page'] = 'register'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')
