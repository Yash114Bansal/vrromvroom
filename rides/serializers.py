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

class RideViewSerializer(serializers.ModelSerializer):
    departure_location = GeometryField()
    destination_location = GeometryField()
    departure_distance = serializers.CharField()
    destination_distance = serializers.CharField()
    driver_name = serializers.CharField(source="user.name", read_only=True)
    driver_phone = serializers.CharField(source="user.phone_number", read_only=True)
    driver_profile_pic = serializers.CharField(source="user.profile_picture", read_only=True)

    class Meta:
        model = RideModel
        fields = ["id","seat_available","departure_location", "destination_location", "departure_distance", "destination_distance",'departure_time', 'fare','driver_name','driver_phone','driver_profile_pic']
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Convert Distance objects to float
        ret['departure_distance'] = instance.departure_distance.m
        ret['destination_distance'] = instance.destination_distance.m
        return ret


class MyRideSerializer(serializers.ModelSerializer):
    departure_location = GeometryField()
    destination_location = GeometryField()
    driver_name = serializers.CharField(source="user.name", read_only=True)
    driver_phone = serializers.CharField(source="user.phone_number", read_only=True)
    driver_profile_pic = serializers.CharField(source="user.profile_picture", read_only=True)

    class Meta:
        model = RideModel
        fields = ["id","seat_available","departure_location", "destination_location",'departure_time', 'fare','driver_name','driver_phone','driver_profile_pic']
