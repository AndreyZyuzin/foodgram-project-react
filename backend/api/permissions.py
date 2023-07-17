import logging

from rest_framework import permissions

logger = logging.getLogger(__name__)


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user == obj.user)


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user == obj.user)
