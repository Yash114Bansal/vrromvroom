from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

class UserDetailsViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='Test@123',
        )
        self.refresh_token = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh_token.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_get_user_details(self):
        # Fetch user details using the API endpoint
        response = self.client.get(reverse('get_user_details'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure the correct user details are returned
        self.assertEqual(response.data['email'], self.user.email)
        # Add more assertions based on your UserDetailsSerializer fields

    def test_unauthenticated_request(self):
        # Remove authentication to simulate an unauthenticated request
        self.client.credentials()

        # Try to fetch user details without authentication
        response = self.client.get(reverse('get_user_details'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
