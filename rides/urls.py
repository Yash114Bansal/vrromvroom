from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import RideViewSet, RideSearchView, RideBookingView

router = DefaultRouter()
router.register(r'', RideViewSet, basename='ride')

urlpatterns = [
    path('search/',RideSearchView.as_view()),
    path('book/<int:ride_id>/', RideBookingView.as_view(), name='ride-book'),  # <-- Updated URL pattern
    path('', include(router.urls)),
]