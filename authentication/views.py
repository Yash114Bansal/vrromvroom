from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.utils import timezone

from random import randint
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from .utils import send_welcome_email
from .models import OTP

from accounts.models import UserProfile

class RegisterView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = UserProfile.objects.filter(email=email, email_verified=False).first()

        if user:
            user.delete()

        # Save the user profile
        user_profile = serializer.save()

        # Checking If Any OTP Exists For The Provided Mail
        old_otp = OTP.objects.filter(user = user_profile)

        # If OTP Exists Delete That OTP
        if old_otp:
                old_otp.delete()

        otp = randint(100000,999999)
        expiry_time = timezone.now() + timezone.timedelta(minutes=5)
        if send_welcome_email(otp, email) == 1:
            OTP.objects.create(user=user_profile,otp=otp,expiry_time=expiry_time,otp_type="email")
        
        else:
                # Email sending failed
                return Response(
                    {"message": "Email sending failed"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )


        # Generate access and refresh tokens
        refresh = RefreshToken.for_user(user_profile)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Return both tokens in the response
        return Response({"access_token": access_token, "refresh_token": refresh_token}, status=status.HTTP_201_CREATED)
