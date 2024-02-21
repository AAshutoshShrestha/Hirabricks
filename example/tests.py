from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Car

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('index')
        self.history_url = reverse('history')
        self.alldatas_url = reverse('alldatas')
        self.analytics_url = reverse('analytics')
        self.profile_url = reverse('profile')
        self.test_url = reverse('test')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.change_password_url = reverse('change_password')

        # Create a test user
        self.user = User.objects.create_user(username='Tunnel-hirabricks', password='hirabricks@123_')

    def test_index_GET(self):
        response = self.client.get(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_history_GET(self):
        response = self.client.get(self.history_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'history.html')

    # Add more test cases for other views...

    def test_login_GET(self):
        response = self.client.get(self.login_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_logout_GET(self):
        response = self.client.get(self.logout_url)

        self.assertEquals(response.status_code, 302)  # Check for redirect after logout
        self.assertRedirects(response, self.login_url)  # Check if redirected back to login page

    def test_change_password_GET(self):
        self.client.login(username='Tunnel-hirabricks', password='_hirabricks@123')
        response = self.client.get(self.change_password_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'updatepassword.html')
