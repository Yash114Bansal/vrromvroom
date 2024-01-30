from rest_framework import serializers
from rest_framework_gis.fields import GeometryField
from .models import RideModel

class RideSerializer(serializers.ModelSerializer):
    departure_location = GeometryField()
    destination_location = GeometryField()

    class Meta:
        model = RideModel
        geo_field = 'departure_location'
        fields = ['id', 'seat_available', 'departure_location', 'destination_location', 'departure_time', 'fare']

class RideSearchSerializer(serializers.Serializer):
    pickup_location = GeometryField()
    destination_location = GeometryField()