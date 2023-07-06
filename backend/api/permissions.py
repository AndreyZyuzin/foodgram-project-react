from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class PermissionsForUsers(permissions.BasePermission):
    """Разрешния для запросов users.
    
    Просматриваются список users авторезированные и админы.
    Разрешается гостям создавать новых пользователей.
    """
    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated and request.user.is_staff
        if view.action == 'create':
            return True
        return False


class isAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user == obj.author)