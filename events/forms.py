from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Event, EventComment
from accounts.models import User


class CreateEventForm(forms.ModelForm):
    participants = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text="Select participants for the event"
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['description'].required = False
        self.fields['end_date'].required = False
        self.fields['location'].required = False
        self.fields['tasks'].required = False

        if user:
            self.fields['participants'].queryset = User.objects.exclude(id=user.id)
        else:
            self.fields['participants'].queryset = User.objects.all()

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
        title = self.cleaned_data.get('title')
        if Event.objects.filter(title=title).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Event with this title already exists.")
        return title

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date > end_date:
                raise ValidationError("Дата початку не може бути пізніше за дату завершення.")

        return cleaned_data


class EventCommentForm(forms.ModelForm):
    class Meta:
        model = EventComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 3, 'class': 'form-control', 'placeholder': 'Write a comment...'
            })
        }
