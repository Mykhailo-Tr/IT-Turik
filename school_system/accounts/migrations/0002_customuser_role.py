# Generated by Django 5.2 on 2025-04-06 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('student', 'Student'), ('teacher', 'Teacher'), ('parent', 'Parent'), ('admin', 'Admin')], default='student', max_length=10),
        ),
    ]
