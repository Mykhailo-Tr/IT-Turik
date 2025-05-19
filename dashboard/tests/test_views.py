from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import Profile

User = get_user_model()

class DashboardViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.teacher_user = User.objects.create_user(username='teacher', password='testpass123', is_teacher=True)
        self.student_user = User.objects.create_user(username='student', password='testpass123', is_student=True)

        # Створюємо профілі, якщо вони потрібні
        Profile.objects.create(user=self.teacher_user)
        Profile.objects.create(user=self.student_user)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # редірект на логін

    def test_dashboard_view_logged_in(self):
        self.client.login(username='teacher', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page'], 'dashboard')

    def test_accounts_view_requires_teacher(self):
        self.client.login(username='student', password='testpass123')
        response = self.client.get(reverse('teacher_accounts'))
        self.assertEqual(response.status_code, 403)  # має бути заборонено

    def test_accounts_view_as_teacher(self):
        self.client.login(username='teacher', password='testpass123')
        response = self.client.get(reverse('teacher_accounts'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page'], 'teacher_accounts')
        self.assertIn(self.student_user, response.context['accounts'])

    def test_create_student_account_get(self):
        self.client.login(username='teacher', password='testpass123')
        response = self.client.get(reverse('create_account', args=['student']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['role'], 'student')

    def test_create_student_account_post(self):
        self.client.login(username='teacher', password='testpass123')
        response = self.client.post(reverse('create_account', args=['student']), {
            'username': 'newstudent',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newstudent').exists())

    def test_delete_account_post(self):
        self.client.login(username='teacher', password='testpass123')
        response = self.client.post(reverse('delete_account', args=[self.student_user.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(id=self.student_user.id).exists())

    def test_edit_account_get(self):
        self.client.login(username='teacher', password='testpass123')
        response = self.client.get(reverse('edit_account', args=[self.student_user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')

    def test_edit_profile_get(self):
        self.client.login(username='teacher', password='testpass123')
        response = self.client.get(reverse('edit_profile', args=[self.student_user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')
