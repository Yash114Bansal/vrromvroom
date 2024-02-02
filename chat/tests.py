# import json
# from channels.testing import WebsocketCommunicator
# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from chat.consumers import LocationConsumer
# from rides.models import RideModel
# from rest_framework_simplejwt.tokens import AccessToken
# from asgiref.sync import sync_to_async

# User = get_user_model()

# class LocationConsumerTests(TestCase):

#     async def disconnect(self, communicator):
#         await communicator.disconnect()

#     async def send_location(self, communicator, latitude, longitude):
#         await communicator.send_json_to({
#             'latitude': latitude,
#             'longitude': longitude,
#         })

#     async def receive_location(self, communicator):
#         response = await communicator.receive_json_from()
#         return response

#     async def create_user(self):
#         user = await sync_to_async(User.objects.create)(
#             email='testuser@akgec.ac.in',
#             password='testpassword',
#             email_verified=True,
#             phone_verified=True,
#             verified_driver=True,
#         )
#         return user

#     async def create_ride(self, user):
#         ride = await sync_to_async(RideModel.objects.create)(
#             user=user,
#             seat_available=2,
#             departure_location="POINT (-74.0059 40.7128)",
#             destination_location="POINT (-74.0059 40.7128)",
#             departure_time="2024-01-30T12:00:00Z",
#             fare=21.0
#         )
#         return ride

#     async def test_location_consumer(self):
#         # Create a user
#         user = await self.create_user()

#         # Create a RideModel object with all necessary values
#         ride = await self.create_ride(user)
#         # Create an access token for the user
#         access_token = AccessToken.for_user(user)

#         communicator = WebsocketCommunicator(LocationConsumer.as_asgi(), f"/ws/chat/{ride.id}/",{"Authorization":f"Bearer {access_token}"})

#         # Connect and authenticate
#         connected, _subr = await communicator.connect()
#         self.assertTrue(connected)

#         # Send a location
#         await self.send_location(communicator, 12.345, 67.890)

#         # Receive and assert the location
#         response = await self.receive_location(communicator)
#         self.assertEqual(response['latitude'], 12.345)
#         self.assertEqual(response['longitude'], 67.890)

#         # Disconnect
#         await self.disconnect(communicator)

#         # Cleanup
#         await communicator.disconnect()

