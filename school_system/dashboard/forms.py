from django import forms
from accounts.models import Subject, Student

from django import forms
from accounts.models import Subject

class AddSubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter subject name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Short description',
                'rows': 2
            })
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)


class AddChildForm(forms.Form):
    student = forms.ModelChoiceField(queryset=Student.objects.none(), label="Select a student")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = Student.objects.exclude(parents__user=self.user)
