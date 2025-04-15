from django.db import models
from accounts.models import User


class Task(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    due_date = models.DateTimeField(blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title


class UserTaskStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'task')

    def __str__(self):
        return f"{self.user.email} - {self.task.name} - {'✔️' if self.is_completed else '❌'}"
    
