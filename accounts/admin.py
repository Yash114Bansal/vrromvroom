from django.contrib import admin
from import_export.admin import ImportExportMixin
from import_export import resources
from .models import UserProfile

class BaseImportExportAdmin(ImportExportMixin, admin.ModelAdmin):
    pass

class UserProfileResource(resources.ModelResource):
    class Meta:
        model = UserProfile
        exclude = ('id', 'last_login', 'is_superuser', 'groups', 'user_permissions')
        import_id_fields=("email",)

@admin.register(UserProfile)
class UserProfileAdmin(BaseImportExportAdmin):
    list_display = ("name","email")
    fields = (
        "name",
        "email",
        "phone_number",
        "password", 
        "profile_picture",
        "email_verified",
        "phone_verified",
        "age",
        "gender",
    )
    resource_class = UserProfileResource

    def save_model(self, request, obj, form, change):

        obj.set_password(form.cleaned_data["password"])
        super().save_model(request, obj, form, change)
