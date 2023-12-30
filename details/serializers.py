from rest_framework import serializers
from accounts.models import UserProfile

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["email","phone_number","profile_picture","age","gender","email_verified","phone_verified"]