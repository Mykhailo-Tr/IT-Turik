from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from accounts.models import User, Subject, Student, Teacher, Parent, UserProfile

class UserModelTest(TestCase):
    def test_create_user_with_email(self):
        user = User.objects.create_user(email='test@example.com', password='test1234')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('test1234'))
        self.assertEqual(user.role, User.Role.STUDENT)

    def test_create_teacher_user(self):
        user = User.objects.create_user(email='teacher@example.com', password='pass', role=User.Role.TEACHER)
        teacher = Teacher.objects.create(user=user)
        self.assertEqual(teacher.user.role, 'teacher')

    def test_create_student_user(self):
        user = User.objects.create_user(email='student@example.com', password='pass', role=User.Role.STUDENT)
        student = Student.objects.create(user=user)
        self.assertEqual(student.user.role, 'student')

    def test_create_parent_user_with_children(self):
        student_user = User.objects.create_user(email='student2@example.com', password='pass', role=User.Role.STUDENT)
        student = Student.objects.create(user=student_user)

        parent_user = User.objects.create_user(email='parent@example.com', password='pass', role=User.Role.PARENT)
        parent = Parent.objects.create(user=parent_user)
        parent.children.add(student)

        self.assertIn(student, parent.children.all())

    def test_subject_creation(self):
        subject = Subject.objects.create(name="Math", description="Algebra and Geometry")
        self.assertEqual(subject.name, "Math")

    def test_teacher_subject_relationship(self):
        user = User.objects.create_user(email='teacher2@example.com', password='pass', role=User.Role.TEACHER)
        teacher = Teacher.objects.create(user=user)
        subject = Subject.objects.create(name="Physics", description="High school physics")
        teacher.subjects.add(subject)
        self.assertIn(teacher, subject.teachers.all())

    def test_user_profile_creation(self):
        user = User.objects.create_user(email='profile@example.com', password='test')
        profile_pic = SimpleUploadedFile(name='test.jpg', content=b'', content_type='image/jpeg')
        profile = UserProfile.objects.create(user=user, profile_picture=profile_pic, bio='This is a test bio.', date_of_birth=timezone.now().date())

        self.assertEqual(profile.user.email, 'profile@example.com')
        self.assertTrue(profile.bio.startswith('This is'))
