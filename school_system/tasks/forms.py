from django import forms
from django.core.exceptions import ValidationError
from .models import Task
from django.utils import timezone


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'content', 'due_date']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        
        existing_task = Task.objects.filter(title=title).exclude(id=self.instance.id)
        if existing_task.exists():
            raise ValidationError("Task with this title already exists.")
        
        return title
    
    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date < timezone.now():
                raise ValidationError("Due date cannot be before task creation date.")
        return due_date
    

class EditTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'content', 'due_date']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Task.objects.filter(title=title).exclude(id=self.instance.id).exists():
            raise ValidationError("Task with this title already exists.")
        return title
    
    
    

    

    