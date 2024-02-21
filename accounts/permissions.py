from rest_framework import permissions

class BasePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.email_verified and request.user.phone_verified

class IsDriver(BasePermission):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.verified_driver
