from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from djoser.permissions import CurrentUserOrAdmin
from django.shortcuts import get_object_or_404


from recipes.models import Ingredient, Tag, Recipe
from users.models import CustomUser
from .serializers import (CustomUserCreateSerializer, CustomUserSerializer,
                          IngredientSerializer, RecipeSerializer,
                          TagSerializer)
from .pagination import CustomUsersPagination
from .permissions import PermissionsForUsers, isAdmin


import logging
logger = logging.getLogger(__name__)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    # serializer_class = CustomUserSerializer
    pagination_class = CustomUsersPagination
    permission_classes = (PermissionsForUsers,)
    http_method_names = ['get', 'post']
    serializer_action_classes = {
        'list': CustomUserSerializer,
        'create': CustomUserCreateSerializer,
    }

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'GET':
            return CustomUserSerializer
        return CustomUserCreateSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ['get']
    permission_classes = (isAdmin, )


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    http_method_names = ['get']
    permission_classes = (isAdmin, )


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        logger.debug('RecipeViewSet.perform_create')
        serializer.save(author=self.request.user)