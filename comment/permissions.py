from rest_framework.permissions import BasePermission, SAFE_METHODS


class Permission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user and (request.user.is_authenticated or request.user.is_staff) and obj.user == request.user:
            return True
        return False

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)