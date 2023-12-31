from random import randint
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.throttling import AnonRateThrottle

from .models import OTP
from .throttles import ResendOTPRateThrottle
from .utils import send_welcome_email
from .serializers import UserSerializer,OTPVerifySerializer
from accounts.models import UserProfile



class RegisterView(GenericAPIView):
    serializer_class = UserSerializer
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user = UserProfile.objects.filter(email=email).first()

        if user:
            if user.email_verified:
                return Response({"error":"User With That Email Alreay Exists"},status=status.HTTP_400_BAD_REQUEST)
            user.delete()

        # Save the user profile
        user_profile = serializer.save()

        # Checking If Any OTP Exists For The Provided Mail
        old_otp = OTP.objects.filter(user=user_profile)

        # If OTP Exists Delete That OTP
        if old_otp:
            old_otp.delete()

        otp = randint(100000, 999999)
        expiry_time = timezone.now() + timezone.timedelta(minutes=5)
        if send_welcome_email(otp, email) == 1:
            OTP.objects.create(user=user_profile, otp=otp, expiry_time=expiry_time, otp_type="email")
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
    
class ResendOTPView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [ResendOTPRateThrottle]

    def post(self, request):
        # Checking If Any OTP Exists For The Provided Mail
        old_otp = OTP.objects.filter(user=request.user)

        # If OTP Exists Delete That OTP
        if old_otp:
            old_otp.delete()

        otp = randint(100000, 999999)
        expiry_time = timezone.now() + timezone.timedelta(minutes=5)

        if send_welcome_email(otp, request.user.email) == 1:
            OTP.objects.create(user=request.user, otp=otp, expiry_time=expiry_time, otp_type="email")
        else:
            # Email sending failed
            return Response(
                {"message": "Email sending failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response({"message": "OTP has been resent successfully"}, status=status.HTTP_200_OK)
    
class EmailVerifyView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OTPVerifySerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp = serializer.validated_data["otp"]
        

        # Check OTP from Database
        try:
            otp_object = OTP.objects.get(user=request.user, otp=otp)

        except OTP.DoesNotExist:
            return Response(
                {"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Check If OTP Is Expired
        if otp_object.has_expired():
            return Response(
                {"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        
        # Deleting Verified OTP
        otp_object.delete()
        
        request.user.email_verified = True
        request.user.save()

        return Response(
                {
                    "message": "Email verified successfully",
                }, status=status.HTTP_200_OK
            )