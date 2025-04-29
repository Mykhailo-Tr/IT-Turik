from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Event
from accounts.models import User


class CreateEventForm(forms.ModelForm):
    participants = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,  # Це поле не є обов'язковим
        help_text="Select participants for the event"
    )
    class Meta:
        model = Event
        fields = ['title', 'event_type', 'description', 'start_date', 'end_date', 'location', 'participants', 'tasks']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'tasks': forms.CheckboxSelectMultiple(),
        }


    def clean_title(self):
        title = self.cleaned_data['title']
        if Event.objects.filter(title=title).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Event with this title already exists.")
        return title

    