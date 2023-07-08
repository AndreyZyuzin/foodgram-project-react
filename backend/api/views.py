from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from djoser.permissions import CurrentUserOrAdmin
from django.shortcuts import get_object_or_404



from recipes.models import Ingredient, Tag, Recipe
from users.models import CustomUser, Subscription
from .serializers import (CustomUserCreateSerializer, CustomUserSerializer,
                          IngredientSerializer, RecipeSerializer,
                          TagSerializer,
                          SubscriptionSerializer,)
from .pagination import CustomUsersPagination, SubscriptionPagination
from .permissions import isAuthor


import logging
logger = logging.getLogger(__name__)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    pagination_class = CustomUsersPagination
    http_method_names = ['get', 'post', 'delete']

    def get_permissions(self):
        permission_classes = []
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        elif self.action == 'create':
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


    def get_serializer_class(self):
        if self.action == 'create':
            return CustomUserCreateSerializer
        return CustomUserSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    # serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = SubscriptionPagination

    @action(detail=False, methods=['GET'])
    def subscriptions(self, request):
        """Список пользователей-последователей."""
        logger.debug(f'!!!!!!!!!! subscriprions2 !!!!!!!!!')
        user = request.user
        queryset = user.follower.all()
        serializer = SubscriptionSerializer(queryset, many=True)
        return Response(serializer.data)


    @action(detail=True, methods=['POST', 'DELETE'])
    def subscribe(self, request, user_id):
        logger.debug(f'!!!!!!!!!! subscriprions3 !!!!!!!!!')
        subscription = get_object_or_404(
            Subscription, id=self.kwargs.get('user_id'))
        return Response(status.HTTP_204_NO_CONTENT)
        

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ['get']
    permission_classes = (IsAdminUser, )


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    http_method_names = ['get']
    permission_classes = (IsAdminUser, )


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        logger.debug('RecipeViewSet.perform_create')
        serializer.save(author=self.request.user)

