from django.urls import path
from .views import AadharUploadView, DrivingLicenseUploadView, ImageWithVehicleUploadView,DocumentVerificationStatus

urlpatterns = [
    path('upload/aadhar/', AadharUploadView.as_view(), name='aadhar-upload'),
    path('upload/driving_license/', DrivingLicenseUploadView.as_view(), name='driving-license-upload'),
    path('upload/image_with_vehicle/', ImageWithVehicleUploadView.as_view(), name='image-with-vehicle-upload'),
    path('status/', DocumentVerificationStatus.as_view(), name='document-verification-status'),
]
