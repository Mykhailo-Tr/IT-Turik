from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'student', _('Student')
        TEACHER = 'teacher', _('Teacher')
        PARENT = 'parent', _('Parent')
        ADMIN = 'admin', _('Admin')
        
    username = None
    email = models.EmailField(_("email address"), unique=True)
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.STUDENT,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
