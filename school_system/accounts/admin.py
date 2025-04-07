from django.contrib import admin
from .models import User, Student, Parent, Teacher, Subject

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(Teacher)
admin.site.register(Subject)