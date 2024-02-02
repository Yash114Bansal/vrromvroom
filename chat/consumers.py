import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from rides.models import RideModel
from rest_framework.exceptions import AuthenticationFailed,PermissionDenied

User = get_user_model()

class LocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.ride_id = self.scope['url_route']['kwargs']['ride_id']
            self.room_group_name = f"chat_{self.ride_id}"

            authorization_header = next((header for header in self.scope.get("headers", []) if header[0] == b"authorization"), None)

            if not authorization_header:
                raise AuthenticationFailed("Authorization header not found")

            token = authorization_header[1].decode("utf-8").split(" ")[1]

            if not token:
                raise AuthenticationFailed("Token not provided")

            user = await self.get_user_from_access_token(token)
            if not user:
                raise AuthenticationFailed("Invalid access token")

            self.scope["user"] = user

            ride = await self.get_ride()
            has_permission_to_join_ride = await self.check_user_in_ride(ride, user)

            if not has_permission_to_join_ride:

                raise PermissionDenied("User Has Not Permission To Join This Ride")
            ride_started = await self.is_ride_started(ride)
            if not ride_started:
                raise PermissionDenied("Ride Is Not Started Yet")
            
            await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
            )
            
            
            await self.accept()
            
        except Exception as e:
            
            await self.close(code=401)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)

            latitude = data.get('latitude')
            longitude = data.get('longitude')
            if latitude is None or not isinstance(latitude, (int, float)):
                raise ValueError("Invalid latitude value")

            if longitude is None or not isinstance(longitude, (int, float)):
                raise ValueError("Invalid longitude value")
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error':"Invalid Json Format"
            }))
            return
        
        except Exception as e:
            await self.send(text_data=json.dumps({
                'error':str(e)
            }))
            return
            
        user_name = self.scope['user'].name if 'user' in self.scope else 'Unknown User'
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'latitude': latitude,
                'longitude':longitude,
                'user_name': user_name,
            }
        )

    async def chat_message(self, event):
        latitude = event.get('latitude')
        longitude = event.get('longitude')
        user_name = event.get('user_name', 'Unknown User')

        await self.send(text_data=json.dumps({
            'latitude' : latitude,
            'longitude': longitude,
            'user': user_name
        }))

    @database_sync_to_async
    def get_user_from_access_token(self, token):
        access_token = AccessToken(token)
        user_id = access_token["user_id"]
        try:
            return User.objects.get(email=user_id)
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def get_ride(self):
        try:
            return RideModel.objects.get(id=self.ride_id)
        except RideModel.DoesNotExist:
            return None

    @database_sync_to_async
    def check_user_in_ride(self, ride, user):
        return ride and (user == ride.user or user in ride.passengers.all())
    
    @database_sync_to_async
    def is_ride_started(self,ride):
        return ride.status == "onway"
