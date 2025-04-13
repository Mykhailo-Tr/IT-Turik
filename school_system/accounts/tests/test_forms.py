from django.test import TestCase
from accounts.forms import StudentSignUpForm, TeacherSignUpForm, ParentSignUpForm
from accounts.models import User
from accounts.models import Subject
from accounts.models import Student

class SignUpFormsTest(TestCase):
    def test_student_signup_form_valid(self):
        form_data = {
            'email': 'student@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '2000-01-01',
        }
        form = StudentSignUpForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.role, User.Role.STUDENT)

    def test_teacher_signup_form_valid(self):
        subject = Subject.objects.create(name="Math")
        form_data = {
            'email': 'teacher@example.com',
            'password1': 'securepass456',
            'password2': 'securepass456',
            'date_of_birth': '1985-05-15',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'subjects': [subject.pk],  # передаємо список id
        }
        form = TeacherSignUpForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)  # додав errors для дебагу
        user = form.save()
        self.assertEqual(user.role, User.Role.TEACHER)

    def test_parent_signup_form_valid(self):
        student_user = User.objects.create_user(
            email="child@example.com",
            password="childpass",
            role=User.Role.STUDENT,
        )
        student = Student.objects.create(user=student_user)

        form_data = {
            'email': 'parent@example.com',
            'password1': 'parentpass789',
            'password2': 'parentpass789',
            'first_name': 'Alice',
            'last_name': 'Johnson',
            'date_of_birth': '1980-08-20',
            'children': [student.pk],  # передаємо список id
        }
        form = ParentSignUpForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()
        self.assertEqual(user.role, User.Role.PARENT)
        