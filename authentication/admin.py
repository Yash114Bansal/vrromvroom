from django.contrib import admin
from .models import OTP,ResetPasswordModel

admin.site.register(OTP)
admin.site.register(ResetPasswordModel)