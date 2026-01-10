from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.


class RegisterTests(APITestCase):

    def test_register(self):
        data = {
            "username": "jude",
            "email": "example159@example.com",
            "password": "password321#",
            "password2": "password321#"
        }

        url = reverse('register')

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.data, dict)


    
class LogoutTests(APITestCase):

    def setUp(self):
        
        self.user = User.objects.create_user(username="jude", email="example159@example.com", password="password321#")
        self.client.force_authenticate(user=self.user)
        
    
    def test_logout(self):
        data = {
            "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2ODEzNDc2MywiaWF0IjoxNzY4MDQ4MzYzLCJqdGkiOiI4NWU4YmRiNWU0ZjM0NzY2YjQ2ZTE5NTY3Mzc5N2RkZiIsInVzZXJfaWQiOiIyIn0.6mRLF9aWOdf8MuFz9wJY4oceCS7s4wa9DXDrM7tqMhs"
        }

        url = reverse('logout')

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data['detail'], 'Token does not belong to this user.')