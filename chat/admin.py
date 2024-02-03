from django.contrib import admin
from accounts.admin import BaseImportExportAdmin
from .models import Chat

@admin.register(Chat)
class ChatAdmin(BaseImportExportAdmin):
    pass
