from django import forms
from django.core.exceptions import ValidationError
from .models import Task


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Task.objects.filter(title=title).exists():
            raise ValidationError("Task with this title already exists.")
        return title
    


    

    