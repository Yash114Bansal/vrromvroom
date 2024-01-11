from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from . import views

urlpatterns = [
    # Token Endpoints
    path("token/generate/", TokenObtainPairView.as_view(), name="token_generate"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Registration and Email Verification
    path("register/", views.RegisterView.as_view(), name="register"),
    path("verify-email/", views.EmailVerifyView.as_view(), name="verify_email"),
    path("resend-email-verification/", views.ResendEmailVerificationView.as_view(), name="resend_email_verification"),

    # Phone Number Verification
    path("send-phone-verification/", views.SendPhoneOTPView.as_view(), name="send_phone_verification"),
    path("verify-phone/", views.PhoneOTPVerifyView.as_view(), name="verify_phone"),

    # Password Reset
    path("reset/send-otp/email/", views.ForgetPasswordEmailSendOTPView.as_view(), name="reset_send_otp_email"),
    path("reset/send-otp/phone/", views.ForgetPasswordPhoneSendOTPView.as_view(), name="reset_send_otp_phone"),
    path("reset/verify-otp/", views.ForgetPasswordVerifyOTPView.as_view(), name="reset_verify_otp"),
    path("reset/", views.UpdatePasswordView.as_view(), name="update_password"),

    # Exchange
    path('social/', include('social_django.urls', namespace='social')),

    path(r'exchange/', views.ExchangeTokenView.as_view()),

]
