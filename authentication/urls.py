from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from . import views

urlpatterns = [
    path("generate/", TokenObtainPairView.as_view()),
    path("verify/", TokenVerifyView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
]
