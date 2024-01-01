from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from accounts.models import UserProfile

class PasswordField(serializers.CharField):
    def to_internal_value(self, data):
        validate_password(data)
        return super().to_internal_value(data)

class UserSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = PasswordField(write_only=True)


    def create(self, validated_data):
        user = UserProfile.objects.create(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class OTPVerifySerializer(serializers.Serializer):
    otp = serializers.CharField()

class PhoneNumberSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ["phone_number"]