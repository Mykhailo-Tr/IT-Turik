from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import User, UserProfile, Subject, Student
from .forms import StudentSignUpForm, TeacherSignUpForm, ParentSignUpForm, UserUpdateForm, UserProfileUpdateForm
from .forms import AddSubjectForm, CreateSubjectForm, AddChildForm
from .forms import LoginForm
from school_system.decorators import teacher_required, student_required
import os


def main_page(request):
    context = {
        'page': 'home',
    }
    return render(request, 'home_page.html', context)


class UserLoginView(LoginView):
    template_name = 'accounts/forms/login.html'
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
    return render(request, 'accounts/forms/register.html', context)


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
    return render(request, 'accounts/forms/delete_account.html', context)


class UserSignUpView(CreateView):
    model = User
    template_name = 'accounts/forms/signup.html'
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
def account_view(request, user_id=None):
    user = User.objects.get(id=request.user.id) if not user_id else get_object_or_404(User, id=user_id)
    user_id = user.id if not user_id else user_id
    profile_user = get_object_or_404(User, id=user_id) if user_id else user
    
    if request.method == "POST":
        if 'add_subject' in request.POST and user.role == 'teacher':
            form = AddSubjectForm(request.POST)
            if form.is_valid():
                subject = form.cleaned_data['subject']
                user.teacher.subjects.add(subject)
                messages.success(request, f"Subject '{subject.name}' added.")
                return redirect('account')

        elif 'create_subject' in request.POST and user.role == 'teacher':
            form = CreateSubjectForm(request.POST)
            if form.is_valid():
                subject = form.save()
                user.teacher.subjects.add(subject)
                messages.success(request, f"Subject '{subject.name}' created and added.")
                return redirect('account')

        elif 'remove_subject' in request.POST and user.role == 'teacher':
            subject_id = request.POST.get('subject_id')
            subject = get_object_or_404(Subject, id=subject_id)
            user.teacher.subjects.remove(subject)
            messages.info(request, f"Subject '{subject.name}' removed.")
            return redirect('account')

        elif 'delete_subject' in request.POST and user.role == 'teacher':
            subject_id = request.POST.get('subject_id')
            subject = get_object_or_404(Subject, id=subject_id)
            user.teacher.subjects.remove(subject)
            subject.delete()
            messages.warning(request, f"Subject '{subject.name}' deleted.")
            return redirect('account')

        elif 'add_child' in request.POST and user.role == 'parent':
            form = AddChildForm(request.POST, user=request.user)
            if form.is_valid():
                child = form.cleaned_data['child']
                user.parent.children.add(child)
                messages.success(request, f"Child '{child.user.get_full_name()}' added.")
                return redirect('account')

        elif 'remove_child' in request.POST and user.role == 'parent':
            child_id = request.POST.get('child_id')
            child = get_object_or_404(Student, user_id=child_id)
            user.parent.children.remove(child)
            messages.info(request, f"Child '{child.user.get_full_name()}' removed.")
            return redirect('account')

    context = {
        'user': user,
        'user_id': user_id,
        'profile_user': profile_user,
        'add_subject_form': AddSubjectForm(user=request.user),
        'create_subject_form': CreateSubjectForm(),
        'add_child_form': AddChildForm(user=request.user),
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
    return render(request, 'accounts/forms/edit_account.html', context)


@login_required
def edit_profile_view(request, user_id=None):
    if user_id:
        if not (request.user.role == 'admin' or request.user.role == 'teacher'):
            return redirect('dashboard_accounts')
        target_user = get_object_or_404(User, id=user_id)
    else:
        target_user = request.user

    profile = get_object_or_404(UserProfile, user=target_user)
    old_photo = profile.profile_picture.path if profile.profile_picture.name != 'profile_pictures/default.png' else None

    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            if 'profile_picture' in request.FILES and old_photo and os.path.exists(old_photo):
                os.remove(old_photo)

            form.save()
            return redirect('profile')
    else:
        form = UserProfileUpdateForm(instance=profile)

    return render(request, 'accounts/forms/edit_profile.html', {
        'form': form,
        'profile': profile,
        'user': target_user
    })
    
@login_required
def delete_profile_photo_view(request, user_id=None):
    if user_id:
        if not (request.user.role == 'admin' or request.user.role == 'teacher'):
            return redirect('dashboard_accounts')
        target_user = get_object_or_404(User, id=user_id)
    else:
        target_user = request.user

    profile = get_object_or_404(UserProfile, user=target_user)

    if profile.profile_picture.name != 'profile_pictures/default.png':
        if os.path.exists(profile.profile_picture.path):
            os.remove(profile.profile_picture.path)
        profile.profile_picture = 'profile_pictures/default.png'
        profile.save()

    return redirect('profile')
