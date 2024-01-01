from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from . import views

urlpatterns = [
    path("token/generate/", TokenObtainPairView.as_view()),
    path("token/verify/", TokenVerifyView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("register/",views.RegisterView.as_view()),
    path("verify-mail/",views.EmailVerifyView.as_view()),
    path("resend-mail/",views.ResendOTPView.as_view()),
    path("verify-phone/send/",views.SendPhoneOTPView.as_view()),
    path("verify-phone/",views.PhoneOTPVerifyView.as_view()),
]
