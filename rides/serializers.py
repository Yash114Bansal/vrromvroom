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

class RideViewSerializer(serializers.Serializer):
    departure_location = GeometryField()
    destination_location = GeometryField()
    departure_distance = serializers.CharField()
    destination_distance = serializers.CharField()
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Convert Distance objects to float
        ret['departure_distance'] = instance.departure_distance.m
        ret['destination_distance'] = instance.destination_distance.m
        return ret