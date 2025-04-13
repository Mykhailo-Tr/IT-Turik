from django.db import models


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateTimeField()

    def __str__(self):
        return self.name
