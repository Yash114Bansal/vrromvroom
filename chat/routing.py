from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from .consumers import ChatConsumer


websocket_urlpatterns = [
    path('ws/chat/<int:ride_id>/', ChatConsumer.as_asgi()),
]