from django.urls import path
from .views import ChatHistoryAPIView
urlpatterns = [
    path("history/",ChatHistoryAPIView.as_view())
]
