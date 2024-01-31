from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import RideViewSet, RideSearchView, RideBookingView, MyRideView, MyPastRideView

router = DefaultRouter()
router.register(r'', RideViewSet, basename='ride')

urlpatterns = [
    path('search/',RideSearchView.as_view()),
    path('book/<int:ride_id>/', RideBookingView.as_view(), name='ride-book'),
    path('my-ride/', MyRideView.as_view(), name='ride-upcoming'),
    path('my-ride/pasts/', MyPastRideView.as_view(), name='ride-past'),
    path('', include(router.urls)),
]