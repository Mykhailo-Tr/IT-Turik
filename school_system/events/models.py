from django.db import models
from accounts.models import User
from django.urls import reverse


class EventManager(models.Manager):
    def get_all_events(self, user):
        events = Event.objects.filter(author=user)
        return events
    
    def get_running_events(self, user):
        events = Event.objects.filter(author=user, start_date__gte=models.functions.Now())
        return events
    

    


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
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events_created')
    tasks = models.ManyToManyField('tasks.Task', related_name='events', blank=True)
    
    objects = EventManager()


    def __str__(self):
        return f"{self.title} ({self.get_event_type_display()})"

    class Meta:
        ordering = ['start_date']
        
    def get_html_url(self):
        url = reverse("callendar_event-detail", args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'


class EventParticipation(models.Model):
    class ResponseChoices(models.TextChoices):
        UNANSWERED = 'unanswered', 'Unanswered'
        ACCEPTED = 'accepted', 'Accepted'
        DECLINED = 'declined', 'Declined'
        LEAVED = 'leaved', 'Leaved'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    response = models.CharField(max_length=10, choices=ResponseChoices.choices, default=ResponseChoices.UNANSWERED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} - {self.event.title} - {self.response}"



class EventComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user.email} on {self.event.title}"

