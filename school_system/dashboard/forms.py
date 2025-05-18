from django import forms
from accounts.models import Subject, Student

class AddSubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

class AddChildForm(forms.Form):
    student = forms.ModelChoiceField(queryset=Student.objects.none(), label="Select a student")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = Student.objects.exclude(parents__user=self.user)
