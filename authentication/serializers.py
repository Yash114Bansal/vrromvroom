from rest_framework import serializers
from accounts.models import UserProfile


class UserSerializer(serializers.Serializer):

    # class Meta:
    #     model = UserProfile
    #     fields = ["email","password"]
    email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, validated_data):
        user = UserProfile.objects.create(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class OTPVerifySerializer(serializers.Serializer):
    otp = serializers.CharField()