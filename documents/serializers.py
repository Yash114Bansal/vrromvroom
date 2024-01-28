from rest_framework import serializers
from .models import AadharCardModel,DrivingLicenseModel,ImageWithVehicleModel

class AadharUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = AadharCardModel
        fields = ["document"]

class DrivingLicenseUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrivingLicenseModel
        fields = ["document"]

class ImageWithVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageWithVehicleModel
        fields = ["document","vehicle_type","plate_number","vehicle_model"]
        
class AadharStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AadharCardModel
        fields = ["id","is_verified","message"]

class DrivingLicenseStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrivingLicenseModel
        fields = ["id","is_verified","message"]

class ImageWithVehicleStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageWithVehicleModel
        fields = ["id","is_verified","message"]