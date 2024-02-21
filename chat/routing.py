from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('ws/location/<int:ride_id>/', consumers.LocationConsumer.as_asgi()),
    path('ws/chat/<str:email>/', consumers.ChatConsumer.as_asgi()),
]