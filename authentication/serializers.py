from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from accounts.models import UserProfile,AKGECEmailValidator

# Custom serializer for password field with password validation
class PasswordField(serializers.CharField):
    def to_internal_value(self, data):
        validate_password(data)
        return super().to_internal_value(data)

# Serializer for creating a new user
class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[AKGECEmailValidator()])
    password = PasswordField(write_only=True)

    def create(self, validated_data):
        # Create a new user profile with the provided email
        user = UserProfile.objects.create(email=validated_data['email'])
        # Set the password for the user
        user.set_password(validated_data['password'])
        user.save()
        return user

# Serializer for OTP verification
class OTPVerifySerializer(serializers.Serializer):
    otp = serializers.CharField()

# Serializer for updating phone number
class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["phone_number"]

# Serializer for initiating password recovery with phone number
class PhoneNumberForgetPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

# Serializer for initiating password recovery with email
class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

# Serializer for handling authentication tokens and OTP
class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()
    otp = serializers.CharField()

# Serializer for updating password with a token
class UpdatePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

# Serializer for handling OAuth2 access tokens in social authentication
class SocialSerializer(serializers.Serializer):
    access_token = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
    )
