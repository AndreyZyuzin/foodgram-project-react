from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class PermissionsForUsers(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated and request.user.is_staff
        if view.action == 'create':
            return True
        return False

