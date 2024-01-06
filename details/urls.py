from django.urls import path
from . import views

urlpatterns = [
    path('user/',views.UserDetailsView.as_view(),name="get_user_details")
]
