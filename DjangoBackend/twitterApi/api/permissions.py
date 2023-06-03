from rest_framework import permissions


class DefaultPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.user_type == "default":
            return True
        return False


class BusinessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.user_type == "business":
            return True
        return False
