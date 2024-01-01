from random import randint
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from .models import OTP
from .throttles import ResendOTPRateThrottle
from .utils import send_welcome_email, send_mobile_otp
from .serializers import UserSerializer, OTPVerifySerializer, PhoneNumberSerializer
from accounts.models import UserProfile


class RegisterView(GenericAPIView):
    serializer_class = UserSerializer
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        # Register user view with email verification
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user = UserProfile.objects.filter(email=email).first()

        if user:
            # If user exists, delete and recreate for a fresh registration
            if user.email_verified:
                return Response(
                    {"error": "User With That Email Already Exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.delete()

        # Save the user profile
        user_profile = serializer.save()

        # Checking If Any OTP Exists For The Provided Mail
        old_otp = OTP.objects.filter(user=user_profile, otp_type="email")

        # If OTP Exists Delete That OTP
        if old_otp:
            old_otp.delete()

        # Generate a random OTP and send a welcome email
        otp = randint(100000, 999999)
        expiry_time = timezone.now() + timezone.timedelta(minutes=5)
        if send_welcome_email(otp, email) == 1:
            OTP.objects.create(
                user=user_profile, otp=otp, expiry_time=expiry_time, otp_type="email"
            )
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
        return Response(
            {"access_token": access_token, "refresh_token": refresh_token},
            status=status.HTTP_201_CREATED,
        )


class ResendOTPView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [ResendOTPRateThrottle]

    def post(self, request):
        # Resend OTP for email verification
        if request.user.email_verified:
            return Response(
                {"message": "Email is Already Verified."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        old_otp = OTP.objects.filter(user=request.user, otp_type="email")

        # If OTP Exists Delete That OTP
        if old_otp:
            old_otp.delete()

        # Generate a new OTP and resend the welcome email
        otp = randint(100000, 999999)
        expiry_time = timezone.now() + timezone.timedelta(minutes=5)

        if send_welcome_email(otp, request.user.email) == 1:
            OTP.objects.create(
                user=request.user, otp=otp, expiry_time=expiry_time, otp_type="email"
            )
        else:
            # Email sending failed
            return Response(
                {"message": "Email sending failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {"message": "OTP has been resent successfully"}, status=status.HTTP_200_OK
        )


class EmailVerifyView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OTPVerifySerializer

    def post(self, request):
        # Verify email using OTP
        if request.user.email_verified:
            return Response(
                {"message": "Email is Already Verified."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp = serializer.validated_data["otp"]

        # Check OTP from Database
        try:
            otp_object = OTP.objects.get(user=request.user, otp=otp, otp_type="email")
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

        # Mark user email as verified
        request.user.email_verified = True
        request.user.save()

        return Response(
            {"message": "Email verified successfully"}, status=status.HTTP_200_OK
        )


class SendPhoneOTPView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [ResendOTPRateThrottle]
    serializer_class = PhoneNumberSerializer

    def post(self, request):
        # Send OTP for phone verification
        if not request.user.email_verified:
            return Response(
                {"message": "Verify Email First."}, status=status.HTTP_400_BAD_REQUEST
            )

        if request.user.phone_verified:
            return Response(
                {"message": "Phone is Already Verified."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data["phone_number"]

        old_otp = OTP.objects.filter(user=request.user, otp_type="phone")

        # If OTP Exists Delete That OTP
        if old_otp:
            old_otp.delete()

        # Generate a new OTP and send it for phone verification
        otp = randint(100000, 999999)
        expiry_time = timezone.now() + timezone.timedelta(minutes=5)

        if send_mobile_otp(otp, phone_number) == 1:
            OTP.objects.create(
                user=request.user, otp=otp, expiry_time=expiry_time, otp_type="phone"
            )
        else:
            return Response(
                {"message": "OTP sending failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {"message": "OTP has been resent successfully"}, status=status.HTTP_200_OK
        )


class PhoneOTPVerifyView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OTPVerifySerializer

    def post(self, request):
        # Verify phone using OTP
        if request.user.phone_verified:
            return Response({"message": "Phone is Already Verified."})

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp = serializer.validated_data["otp"]

        # Check OTP from Database
        try:
            otp_object = OTP.objects.get(user=request.user, otp=otp, otp_type="phone")
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

        # Mark user phone as verified
        request.user.phone_verified = True
        request.user.save()

        return Response(
            {"message": "Phone verified successfully"}, status=status.HTTP_200_OK
        )
