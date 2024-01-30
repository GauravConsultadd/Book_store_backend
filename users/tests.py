from django.test import TestCase
from .models import CustomUser
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

# Create your tests here.
class LoginViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = 'http://localhost:8000/users/login'  # Assuming you have a named URL for login

        # Create a user for testing
        self.user = CustomUser.objects.create_buyer(
            username='testuser',
            email='testuser@example.com',
            password='testpassword',
            role='Buyer'
        )

    def test_login_successful(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword',
        }

        response = self.client.post(self.login_url,data,format='json',follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)