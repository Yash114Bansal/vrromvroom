from django.contrib import admin
from accounts.admin import BaseImportExportAdmin
from .models import RideModel

@admin.register(RideModel)
class RideModelAdmin(BaseImportExportAdmin):
    pass
