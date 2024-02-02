from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('ws/chat/<int:ride_id>/', consumers.LocationConsumer.as_asgi()),
]