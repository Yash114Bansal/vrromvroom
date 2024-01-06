from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient,APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterUserTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_view_valid_data(self):
        url = reverse('register')
        data = {'email': 'test@akgec.ac.in', 'password': 'Password@123'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)

    def test_register_view_invalid_email(self):
        url = reverse('register')
        data = {'email': 'invalid@example.com', 'password': 'Password@123'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_register_view_invalid_password(self):
        url = reverse('register')
        data = {'email': 'test@akgec.ac.in', 'password': '987987879'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

class TokenGenerationTests(APITestCase):

    def setUp(self):
        self.user_data = {'email': 'test@akgec.ac.in', 'password': 'Password@123'}
        self.user = get_user_model().objects.create_user(**self.user_data)
        self.token_url = reverse('token_generate')

    def test_token_generation(self):
        data = {'email': self.user_data['email'], 'password': self.user_data['password']}
        response = self.client.post(self.token_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_verification(self):
        # Generate a token for the user
        refresh = RefreshToken.for_user(self.user)
        token = {'token': str(refresh)}

        # Verify the token
        response = self.client.post(reverse('token_verify'), token, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_refresh(self):
        # Generate a token for the user
        refresh = RefreshToken.for_user(self.user)
        token = {'refresh': str(refresh)}

        # Refresh the token
        response = self.client.post(reverse('token_refresh'), token, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)


