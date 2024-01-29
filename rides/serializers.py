from rest_framework import serializers
from .models import RideModel

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideModel
        fields = ['id', 'seat_available', 'departure_location', 'destination_location', 'departure_time', 'fare']
