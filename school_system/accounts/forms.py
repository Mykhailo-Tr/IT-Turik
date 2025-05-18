from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from .models import User, Student, Teacher, Parent, Subject, UserProfile



class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        required=True,
        label='Email address',
        max_length=254,
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email', 
            'autofocus': True
        })
    )
    
    password = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'})
    )
    

class BaseSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label='First Name')
    last_name = forms.CharField(max_length=30, required=True, label='Last Name')
    
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Date of Birth'
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name', 'date_of_birth', 'password1', 'password2')

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        today = timezone.now().date()

        if dob > today:
            raise ValidationError("Date of birth cannot be in the future.")
        
        min_age = 5  # мінімальний вік, наприклад 5 років
        if dob > today - timedelta(days=min_age * 365):
            raise ValidationError(f"User must be at least {min_age} years old.")
        
        return dob

    def save_user(self, role):
        user = super().save(commit=False)
        user.role = role
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        
        UserProfile.objects.create(
            user=user,
            date_of_birth=self.cleaned_data.get('date_of_birth')
        )
        return user



class StudentSignUpForm(BaseSignUpForm):
    @transaction.atomic
    def save(self):
        user = self.save_user('student')
        Student.objects.create(user=user)
        return user


class TeacherSignUpForm(BaseSignUpForm):
    subjects = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(), 
                                              widget=forms.CheckboxSelectMultiple, 
                                              required=False)

    @transaction.atomic
    def save(self):
        user = self.save_user('teacher')
        Teacher.objects.create(user=user)
        return user


class ParentSignUpForm(BaseSignUpForm):
    children = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Select Children"
    )

    @transaction.atomic
    def save(self):
        user = self.save_user('parent')
        parent = Parent.objects.create(user=user)
        parent.children.set(self.cleaned_data['children'])  # Додаємо зв'язок з дітьми
        return user

    
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
        


class UserProfileUpdateForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Date of Birth'
    )
    
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio', 'date_of_birth']
        
    def save(self, commit=True):
        user_profile = super().save(commit=False)
        if commit:
            user_profile.save()
        return user_profile


