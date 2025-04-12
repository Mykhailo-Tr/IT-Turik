from django.test import TestCase
from accounts.models import User

class CustomUserManagerTest(TestCase):
    def test_create_user_success(self):
        user = User.objects.create_user(email='normal@example.com', password='abc123')
        self.assertEqual(user.email, 'normal@example.com')
        self.assertTrue(user.check_password('abc123'))
        self.assertEqual(user.role, 'student')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser_success(self):
        admin = User.objects.create_superuser(email='admin@example.com', password='adminpass')
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertEqual(admin.role, 'admin')

    def test_create_user_no_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='somepass')
