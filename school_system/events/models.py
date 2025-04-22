from django.db import models
from tasks.models import Task
from accounts.models import User


class Event(models.Model):
    title = models.CharField(max_length=100)
    event_type = models.CharField(max_length=50, choices=[
        ('exam', 'Exam'),
        ('test_work', 'Test Work'),
        ('school_meeting', 'School meeting'),
        ('parent_meeting', 'Parent meeting'),
        ('personal_meeting', 'Personal meeting'),
    ])

    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    participants = models.ManyToManyField(User, related_name='events_joined', blank=True)
    tasks = models.ManyToManyField(Task, related_name='events', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events_created')


    def __str__(self):
        return self.title
