from django.contrib import admin
from accounts.admin import BaseImportExportAdmin
from .models import AadharCardModel, DrivingLicenseModel, ImageWithVehicleModel

@admin.register(AadharCardModel)
class AadharCardAdmin(BaseImportExportAdmin):
    pass

@admin.register(DrivingLicenseModel)
class DrivingLicenseAdmin(BaseImportExportAdmin):
    pass

@admin.register(ImageWithVehicleModel)
class ImageWithVehicleAdmin(BaseImportExportAdmin):
    pass