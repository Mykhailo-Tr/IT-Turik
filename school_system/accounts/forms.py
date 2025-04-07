from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Student, Teacher, Parent, Subject
from django.db import transaction


class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'password1', 'password2')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.role = 'student'
        user.save()
        student = Student.objects.create(user=user)
        return user
    

class TeacherSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    subjects = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(), widget=forms.CheckboxSelectMultiple)
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'password1', 'password2')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.role = 'teacher'
        user.save()
        teacher = Teacher.objects.create(user=user)
        return user
    

class ParentSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    children = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(), 
        widget=forms.CheckboxSelectMultiple
    )
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'password1', 'password2')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.role = 'parent'
        user.save()
        parent = Parent.objects.create(user=user)
        return user


        