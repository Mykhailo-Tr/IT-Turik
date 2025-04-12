from django.test import TestCase
from django.urls import reverse
from accounts.models import User

class AuthViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='loginuser@example.com', password='password123')

    def test_login_view_valid_user(self):
        response = self.client.post(reverse('login'), {'email': 'loginuser@example.com', 'password': 'password123'})
        self.assertRedirects(response, reverse('home'))

    def test_login_view_invalid_credentials(self):
        response = self.client.post(reverse('login'), {'email': 'wrong@example.com', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, 302)  # redirect to login
        self.assertRedirects(response, reverse('login'))

    def test_logout_view(self):
        self.client.login(email='loginuser@example.com', password='password123')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('home'))

    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_account_view_requires_login(self):
        response = self.client.get(reverse('account'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('account')}")

    def test_delete_account_post(self):
        self.client.login(email='loginuser@example.com', password='password123')
        response = self.client.post(reverse('delete_account'))
        self.assertRedirects(response, reverse('home'))
        self.assertFalse(User.objects.filter(email='loginuser@example.com').exists())
