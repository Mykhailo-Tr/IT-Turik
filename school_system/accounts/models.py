from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager



class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'student', 'Student'
        TEACHER = 'teacher', 'Teacher'
        PARENT = 'parent', 'Parent'
        ADMIN = 'admin', 'Admin'
        
    username = None
    email = models.EmailField("email address", unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
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
    

class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name
    
    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    def __str__(self):
        return self.user.email


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    subjects = models.ManyToManyField(Subject, related_name='teachers')
    
    def __str__(self):
        return self.user.email
    
    
class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    children = models.ManyToManyField(Student, related_name='parents')
    
    def __str__(self):
        return self.user.email
    
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.user.email
