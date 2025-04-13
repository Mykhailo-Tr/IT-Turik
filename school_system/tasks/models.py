from django.db import models
from accounts.models import User


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateTimeField()

    def __str__(self):
        return self.name


class UserTaskStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'task')

    def __str__(self):
        return f"{self.user.email} - {self.task.name} - {'✔️' if self.is_completed else '❌'}"