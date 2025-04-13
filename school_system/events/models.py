from django.db import models
from tasks.models import Task


class Event(models.Model):
    name = models.CharField(max_length=100)
    event_type = models.CharField(max_length=50, choices=[
        ('exam', 'Exam'),
        ('test_work', 'Test Work'),
        ('school_meeting', 'School meeting'),
        ('parent_meeting', 'Parent meeting'),
        ('personal_meeting', 'Personal meeting'),
    ])

    description = models.TextField()
    start_date = models.DateTimeField()
    duration = models.DurationField()
    location = models.CharField(max_length=255)
    participants = models.ManyToManyField('accounts.User', related_name='events', blank=True)
    tasks = models.ManyToManyField(Task, related_name='events', blank=True)


    def __str__(self):
        return self.name
    

