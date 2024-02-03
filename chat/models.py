from django.db import models
from accounts.models import UserProfile
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

class Chat(models.Model):
    content = models.TextField()
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_chats')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_chats')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} to {self.receiver} at {self.timestamp}"
    
    class Meta:
        unique_together = ['sender', 'receiver']
