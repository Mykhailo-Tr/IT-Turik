from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Event
from accounts.models import User



class CreateEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'event_type', 'description', 'start_date', 'end_date', 'location', 'participants', 'tasks']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'participants': forms.CheckboxSelectMultiple(),
            'tasks': forms.CheckboxSelectMultiple(),
        }
        

    def clean_title(self):
        title = self.cleaned_data.get('title')

        existing_task = Event.objects.filter(title=title).exclude(id=self.instance.id)
        if existing_task.exists():
            raise ValidationError("Event with this title already exists.")

        return title
    


    