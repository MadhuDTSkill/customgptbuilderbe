from rest_framework.permissions import BasePermission

class IsUserIDAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and isinstance(request.user, str))
