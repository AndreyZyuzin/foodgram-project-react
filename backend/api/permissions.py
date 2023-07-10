from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


import logging
logger = logging.getLogger(__name__)


class isAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user == obj.user)
    


class isAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user == obj.user)

