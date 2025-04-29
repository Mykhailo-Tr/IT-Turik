from django.db import models
from tasks.models import Task
from accounts.models import User


class Event(models.Model):
    class EventType(models.TextChoices):
        EXAM = 'exam', 'Exam'
        TEST_WORK = 'test_work', 'Test Work'
        SCHOOL_MEETING = 'school_meeting', 'School Meeting'
        PARENT_MEETING = 'parent_meeting', 'Parent Meeting'
        PERSONAL_MEETING = 'personal_meeting', 'Personal Meeting'

    title = models.CharField(max_length=100)
    event_type = models.CharField(max_length=50, choices=EventType.choices)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    participants = models.ManyToManyField(User, related_name='events_joined', blank=True)
    tasks = models.ManyToManyField(Task, related_name='events', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events_created')

    def __str__(self):
        return f"{self.title} ({self.get_event_type_display()})"

    class Meta:
        ordering = ['start_date']
