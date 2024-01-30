from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import RideViewSet, RideSearchView

router = DefaultRouter()
router.register(r'', RideViewSet, basename='ride')

urlpatterns = [
    path('search/',RideSearchView.as_view()),
    path('', include(router.urls)),
]