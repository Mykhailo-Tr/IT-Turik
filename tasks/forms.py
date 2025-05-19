from django import forms
from django.core.exceptions import ValidationError
from .models import Task
from django.utils import timezone


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'content', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].required = False
        self.fields['due_date'].required = False

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Task.objects.filter(title=title).exclude(id=self.instance.id).exists():
            raise ValidationError("Task with this title already exists.")
        return title

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date < timezone.now():
            raise ValidationError("Due date cannot be before current time.")
        return due_date

