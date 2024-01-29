from django.urls import path
from .views import RideCreateView, RideDeleteView, MyRidesView

urlpatterns = [
    path('', RideCreateView.as_view(), name='ride-create'),
    path('<int:pk>/delete/', RideDeleteView.as_view(), name='ride-delete'),
    path('my-rides/', MyRidesView.as_view(), name='my-rides'),
]
