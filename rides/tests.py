from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import RideModel
from .serializers import RideSerializer
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class RideViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@akgec.ac.in', password='testpassword', email_verified=True, phone_verified=True, verified_driver=True)
        self.client.force_authenticate(user=self.user)
        self.url =  reverse('ride-list')

    def test_create_ride(self):
        data = {
            'seat_available': 3,
            'departure_location': {
                'type': 'Point',
                'coordinates': [0, 0]
            },
            'destination_location': {
                'type': 'Point',
                'coordinates': [1, 1]
            },
            'departure_time': '2024-01-30T12:00:00Z',
            'fare': 20.0
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RideModel.objects.count(), 1)

    def test_create_ride_with_existing_ride(self):
        RideModel.objects.create(user=self.user, seat_available=2,departure_location="POINT (-74.0059 40.7128)", destination_location="POINT (-74.0059 40.7128)",departure_time="2024-01-30T12:00:00Z",fare=21.0)
        data = {
            'seat_available': 3,
            'departure_location': {
                'type': 'Point',
                'coordinates': [0, 0]
            },
            'destination_location': {
                'type': 'Point',
                'coordinates': [1, 1]
            },
            'departure_time': '2024-01-30T12:00:00Z',
            'fare': 20.0
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(RideModel.objects.count(), 1)

    def test_update_ride(self):
        ride = RideModel.objects.create(user=self.user, seat_available=2,departure_location="POINT (-74.0059 40.7128)", destination_location="POINT (-74.0059 40.7128)",departure_time="2024-01-30T12:00:00Z",fare=21.0)
        data = {
            'seat_available': 3,
            'departure_location': {
                'type': 'Point',
                'coordinates': [0, 0]
            },
            'destination_location': {
                'type': 'Point',
                'coordinates': [1, 1]
            },
            'departure_time': '2024-01-30T12:00:00Z',
            'fare': 20.0
        }
        print(self.url)
        response = self.client.put(f'{self.url}{ride.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ride.refresh_from_db()
        self.assertEqual(ride.seat_available, 3)

    def test_delete_ride(self):
        ride = RideModel.objects.create(user=self.user, seat_available=2,departure_location="POINT (-74.0059 40.7128)", destination_location="POINT (-74.0059 40.7128)",departure_time="2024-01-30T12:00:00Z",fare=21.0)

        response = self.client.delete(f'{self.url}{ride.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(RideModel.objects.count(), 0)

    def test_delete_ride_with_unauthorized_user(self):
        another_user = User.objects.create_user(email='anotheruser@akgec.ac.in', password='anotherpassword')
        ride = RideModel.objects.create(user=another_user, seat_available=2)

        response = self.client.delete(f'{self.url}{ride.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(RideModel.objects.count(), 1)

class RideSerializerTest(APITestCase):
    def test_ride_serializer(self):
        data = {
            'seat_available': 3,
            'departure_location': {
                'type': 'Point',
                'coordinates': [0, 0]
            },
            'destination_location': {
                'type': 'Point',
                'coordinates': [1, 1]
            },
            'departure_time': '2024-01-30T12:00:00Z',
            'fare': 20.0
        }

        serializer = RideSerializer(data=data)
        self.assertTrue(serializer.is_valid())
