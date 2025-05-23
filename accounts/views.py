from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import User, UserProfile, Subject, Student
from .forms import StudentSignUpForm, TeacherSignUpForm, ParentSignUpForm, UserUpdateForm, UserProfileUpdateForm
from .forms import LoginForm
from school_system.decorators import teacher_required, student_required
import os


class HomeView(TemplateView):
    template_name = 'home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'home'
        return context


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


class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')


class RegisterView(TemplateView):
    template_name = 'accounts/forms/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'register'
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class DeleteAccountView(View):
    def get(self, request, user_id=None):
        if user_id:
            if not (request.user.role == 'admin' or request.user.role == 'teacher'):
                return redirect('dashboard_accounts')
            user = get_object_or_404(User, id=user_id)
        else:
            user = request.user

        previous_url = request.META.get('HTTP_REFERER', reverse('account'))

        context = {
            'page': 'delete_account',
            'user': user,
            'previous_url': previous_url,
        }
        return render(request, 'accounts/forms/delete_account.html', context)

    def post(self, request, user_id=None):
        if user_id:
            if not (request.user.role == 'admin' or request.user.role == 'teacher'):
                return redirect('dashboard_accounts')
            user = get_object_or_404(User, id=user_id)
        else:
            user = request.user

        if not user_id:
            logout(request)

        user.delete()

        if user_id:
            messages.success(request, f'Account {user.get_full_name()} has been deleted successfully.')
            return redirect('dashboard_accounts')
        else:
            messages.success(request, 'Your account has been deleted successfully.')
            return redirect('home')


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


@method_decorator(login_required(login_url='login'), name='dispatch')
class AccountView(View):
    def get(self, request, user_id=None):
        user = get_object_or_404(User, id=user_id) if user_id else request.user
        profile_user = get_object_or_404(UserProfile, user=user)

        context = {
            'user': user,
            'user_id': user.id,
            'profile_user': profile_user,
        }
        return render(request, 'accounts/account.html', context)


@method_decorator(login_required(login_url='login'), name='dispatch')
class ProfileView(View):
    def get(self, request, user_id=None):
        if user_id:
            if not (request.user.role == 'admin' or request.user.role == 'teacher'):
                return redirect('dashboard_accounts')
            target_user = get_object_or_404(User, id=user_id)
        else:
            target_user = request.user

        context = {
            'page': 'profile',
            'user': target_user,
            'profile': target_user.profile,  # важливо — профіль саме того користувача
        }
        return render(request, 'accounts/profile.html', context)



class AccountUpdateView(View):
    def get_user(self, request, user_id):
        """Допоміжний метод для отримання користувача з урахуванням ролей"""
        if user_id:
            if not (request.user.role in ['admin', 'teacher']):
                return None
            return get_object_or_404(User, id=user_id)
        return request.user

    def get(self, request, user_id=None):
        user = self.get_user(request, user_id)
        if not user:
            return redirect('dashboard_accounts')

        form = UserUpdateForm(instance=user)
        context = {
            'page': 'edit_account',
            'form': form,
            'previous_url': request.META.get('HTTP_REFERER', reverse('account')),
        }
        return render(request, 'accounts/forms/edit_account.html', context)

    def post(self, request, user_id=None):
        user = self.get_user(request, user_id)
        if not user:
            return redirect('dashboard_accounts')

        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            if user_id:
                messages.success(request, f'Account {user.get_full_name()} has been updated.')
                return redirect('account', user_id=user_id)
            else:
                messages.success(request, 'Your account has been updated.')
                return redirect('account')

        context = {
            'page': 'edit_account',
            'form': form,
            'previous_url': request.META.get('HTTP_REFERER', reverse('account')),
        }
        return render(request, 'accounts/forms/edit_account.html', context)



@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(View):
    def get_target_user(self, request, user_id):
        """Отримати цільового користувача"""
        if user_id:
            if request.user.role not in ['admin', 'teacher']:
                return None
            return get_object_or_404(User, id=user_id)
        return request.user

    def get(self, request, user_id=None):
        target_user = self.get_target_user(request, user_id)
        if not target_user:
            return redirect('dashboard_accounts')

        profile = get_object_or_404(UserProfile, user=target_user)
        form = UserProfileUpdateForm(instance=profile)

        return render(request, 'accounts/forms/edit_profile.html', {
            'form': form,
            'profile': profile,
            'user': target_user,
            'previous_url': request.META.get('HTTP_REFERER', reverse('account'))
        })

    def post(self, request, user_id=None):
        target_user = self.get_target_user(request, user_id)
        if not target_user:
            return redirect('dashboard_accounts')

        profile = get_object_or_404(UserProfile, user=target_user)
        old_photo = profile.profile_picture.path if profile.profile_picture.name != 'profile_pictures/default.png' else None

        form = UserProfileUpdateForm(request.POST, request.FILES, instance=profile)
        print("FILES:", request.FILES)
        print("Form valid:", form.is_valid())
        print("Form errors:", form.errors)

        if form.is_valid():
            if 'profile_picture' in request.FILES and old_photo and os.path.exists(old_photo):
                os.remove(old_photo)

            form.save()
            if user_id:
                messages.success(request, f'Profile {target_user.get_full_name()} has been updated successfully.')
                return redirect('account', user_id=user_id)
            else:
                messages.success(request, 'Your profile has been updated successfully.')
                return redirect('profile')

        return render(request, 'accounts/forms/edit_profile.html', {
            'form': form,
            'profile': profile,
            'user': target_user,
            'previous_url': request.META.get('HTTP_REFERER', reverse('account'))
        })
    
    
class DeleteProfilePhotoView(LoginRequiredMixin, View):
    def get(self, request, user_id=None):
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

        return redirect('profile', user_id=target_user.id) if user_id else redirect('profile')