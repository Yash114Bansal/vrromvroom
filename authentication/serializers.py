from rest_framework import serializers
from accounts.models import UserProfile


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ["email","password"]

    def create(self, validated_data):
        user = UserProfile.objects.create(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user