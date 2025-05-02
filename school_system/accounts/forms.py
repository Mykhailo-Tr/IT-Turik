from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
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



class AddSubjectForm(forms.Form):
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), label="Select Subject")
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and hasattr(user, 'teacher'):
            self.fields['subject'].queryset = Subject.objects.exclude(id__in=user.teacher.subjects.values_list('id', flat=True))


class CreateSubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']


class AddChildForm(forms.Form):
    child = forms.ModelChoiceField(queryset=Student.objects.none(), label="Select Child")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and hasattr(user, 'parent'):
            self.fields['child'].queryset = Student.objects.exclude(user_id__in=user.parent.children.values_list('user_id', flat=True))

