from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import AadharCardModel, DrivingLicenseModel, ImageWithVehicleModel
from .serializers import AadharUploadSerializer,DrivingLicenseUploadSerializer,ImageWithVehicleSerializer,DrivingLicenseStatusSerializer,AadharStatusSerializer,ImageWithVehicleStatusSerializer
from rest_framework.parsers import MultiPartParser

class AadharUploadView(CreateAPIView,DestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = AadharUploadSerializer
    parser_classes = [MultiPartParser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_object(self):
        return AadharCardModel.objects.get(user=self.request.user)

class DrivingLicenseUploadView(CreateAPIView,DestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = DrivingLicenseUploadSerializer
    parser_classes = [MultiPartParser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def get_object(self):
        return DrivingLicenseModel.objects.get(user=self.request.user)


class ImageWithVehicleUploadView(CreateAPIView,DestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = ImageWithVehicleSerializer
    parser_classes = [MultiPartParser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_object(self):
        return ImageWithVehicleModel.objects.get(user=self.request.user)

class DocumentVerificationStatus(APIView):
    def get(self, request, *args, **kwargs):

        aadhar_status = AadharCardModel.objects.filter(user=request.user).first()
        driving_license_status = DrivingLicenseModel.objects.filter(user=request.user).first()
        image_with_vehicle_status = ImageWithVehicleModel.objects.filter(user=request.user).first()

        aadhar_serializer = AadharStatusSerializer(aadhar_status) if aadhar_status else None
        driving_license_serializer = DrivingLicenseStatusSerializer(driving_license_status) if driving_license_status else None
        image_with_vehicle_serializer = ImageWithVehicleStatusSerializer(image_with_vehicle_status) if image_with_vehicle_status else None

        data = {
            'aadhar_card': aadhar_serializer.data if aadhar_serializer else None,
            'driving_license': driving_license_serializer.data if driving_license_serializer else None,
            'image_with_vehicle': image_with_vehicle_serializer.data if image_with_vehicle_serializer else None,
        }

        return Response(data, status=status.HTTP_200_OK)