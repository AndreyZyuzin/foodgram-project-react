from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from djoser.permissions import CurrentUserOrAdmin
from django.shortcuts import get_object_or_404



from recipes.models import Favorite, Ingredient, Tag, Recipe
from users.models import CustomUser, Subscription
from .serializers import (CustomUserCreateSerializer, CustomUserSerializer,
                          FavoriteSerializer, IngredientSerializer,
                          RecipeSerializer, RecipeShortSerializer,
                          TagSerializer, SubscriptionSerializer,)
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
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = SubscriptionPagination

    @action(detail=False, methods=['GET'])
    def subscriptions(self, request):
        """Список пользователей-последователей."""
        logger.debug(f'!!!!!!!!!! subscriprions2 !!!!!!!!!')
        queryset = self.filter_queryset(self.get_queryset())
        user = request.user
        queryset = user.follower.all()
        page = self.paginate_queryset(queryset)
        context = self.get_serializer_context()
        serializer_class = self.get_serializer_class()
        if page is None:
            serializer = serializer_class(queryset, many=True, context=context)
            return Response(serializer.data)
        serializer = serializer_class(page, many=True, context=context)
        return self.get_paginated_response(serializer.data)


    def subscriptions2(self, request):
        """Список пользователей-последователей."""
        user = request.user
        queryset = user.follower.all()
        serializer = SubscriptionSerializer(queryset, many=True)
        return Response(serializer.data)


    @action(detail=True, methods=['POST', 'DELETE'])
    def subscribe(self, request, user_id):
        logger.debug(f'!!!!!!!!!! subscriprions3 !!!!!!!!!')
        author = request.user
        is_subscription = Subscription.objects.filter(
            author=author, following__id=user_id).exists()
        if request.method=='POST' and not is_subscription:
            user = CustomUser.objects.get(pk=user_id)
            subscription = Subscription.objects.create(
                author=author, following=user)
            logger.debug(f'id::{id}')
            serializer = SubscriptionSerializer(
                Subscription.objects.get(id=subscription.id))
            return Response(serializer.data)
        if request.method=='DELETE' and is_subscription:
            Subscription.objects.get(
                author=author, following__id=user_id).delete()
            return Response()
        return Response('Подписка осталось как было')
        

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


    @action(detail=True, methods=['POST', 'DELETE'])
    def favorite(self, request, pk=None):
        """Добавление и удаление рецепта pk в избранное пользователя."""
        logger.debug(f'!!!!!!!!!! favorite !!!!!!!!!')
        logger.debug(f'favorite:\nself:{self}\nrequest:{request}\npk:{pk}')
        user = request.user
        is_favorite = Favorite.objects.filter(user=user, recipe=pk).exists()
        logger.debug(f'is_favorite: {is_favorite}')
        if request.method == 'POST':
            recipe = Recipe.objects.get(id=pk)
            favorite, created = Favorite.objects.get_or_create(
                user=user, recipe=recipe)
            if created:
                serializer = RecipeShortSerializer(
                    Recipe.objects.get(id=recipe.id))
                return Response(serializer.data)
        if request.method == 'DELETE' and is_favorite:
            Favorite.objects.get(user=user, recipe=pk).delete()
            return Response('удалено')
            
        return Response('осталось как было')


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)

