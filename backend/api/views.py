import io
import logging

from django.db.models import Sum
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from api.filters import IngredientFilter, RecipeFilter
from api.pagination import (CustomUsersPagination, RecipesPagination,
                            SubscriptionPagination)
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (CustomUserCreateSerializer, CustomUserSerializer,
                             IngredientSerializer, RecipeSerializer,
                             RecipeShortSerializer, SubscriptionSerializer,
                             TagSerializer)

from core.utilites.pdf import PDF

from recipes.models import Cart, Favorite, Ingredient, Recipe, Tag

from users.models import CustomUser, Subscription

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
        queryset = self.filter_queryset(self.get_queryset())
        user = request.user
        queryset = user.following.all()
        page = self.paginate_queryset(queryset)
        context = self.get_serializer_context()
        serializer_class = self.get_serializer_class()
        if page is None:
            serializer = serializer_class(queryset, many=True, context=context)
            return Response(serializer.data)
        serializer = serializer_class(page, many=True, context=context)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['POST', 'DELETE'])
    def subscribe(self, request, author_id):
        user = request.user
        author = CustomUser.objects.get(pk=author_id)
        is_subscription = Subscription.objects.filter(
            user=author, following=user).exists()
        if request.method == 'POST' and not is_subscription:
            subscription = Subscription.objects.create(
                user=author, following=user)
            serializer = SubscriptionSerializer(
                Subscription.objects.get(id=subscription.id))
            return Response(serializer.data)
        if request.method == 'DELETE' and not is_subscription:
            Subscription.objects.get(
                user=author, following=user).delete()
            return Response()
        return Response('Подписка осталось как было')


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ['get']
    permission_classes = (AllowAny, )


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    http_method_names = ['get']
    permission_classes = (AllowAny, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('-pub_date')
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = RecipesPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True,
            methods=['POST', 'DELETE'],
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk=None):
        """Добавление и удаление рецепта pk в избранное пользователя."""
        user = request.user
        is_favorite = Favorite.objects.filter(user=user, recipe=pk).exists()
        if request.method == 'POST':
            recipe = Recipe.objects.get(id=pk)
            favorite, created = Favorite.objects.get_or_create(
                user=user, recipe=recipe)
            if created:
                serializer = RecipeShortSerializer(
                    Recipe.objects.get(id=recipe.id))
                return Response(serializer.data)
        if request.method == 'DELETE' and not is_favorite:
            Favorite.objects.get(user=user, recipe=pk).delete()
            return Response()

        return Response('осталось как было')

    @action(detail=True,
            methods=['POST', 'DELETE'],
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk=None):
        """Добавление и удаление рецепта pk в корзину."""
        user = request.user
        is_cart = Cart.objects.filter(user=user, recipe=pk).exists()
        logger.debug(f'is_cart: {is_cart}')
        if request.method == 'POST':
            recipe = Recipe.objects.get(id=pk)
            cart, created = Cart.objects.get_or_create(
                user=user, recipe=recipe)
            if created:
                serializer = RecipeShortSerializer(
                    Recipe.objects.get(id=recipe.id))
                return Response(serializer.data)
        if request.method == 'DELETE' and is_cart:
            Cart.objects.get(user=user, recipe=pk).delete()
            return Response(f'{user} удаление рецепта из корзины')

        return Response(f'{user} осталось как было')

    @action(detail=False,
            methods=['GET'],
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        """Загрузить файл корзины."""

        user = request.user
        recipes = user.cart.all()
        result = (recipes.values(
            'recipe__ingredients__parametrs__name',
            'recipe__ingredients__parametrs__measurement_unit'
        ).annotate(amount=Sum('recipe__ingredients__amount')))
        ingredients = [
            {'name': item['recipe__ingredients__parametrs__name'],
             'amount': item['amount'],
             'unit': item['recipe__ingredients__parametrs__measurement_unit']
             } for item in result]
        logger.debug(ingredients)

        file_pdf = PDF().creaete_list_ingredients(ingredients,)
        return FileResponse(io.BytesIO(file_pdf),
                            as_attachment=True,
                            filename="ingredients.pdf")

    @action(detail=False,
            methods=['GET'],
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart2(self, request):
        """Загрузить файл корзины."""
        user = request.user
        recipes = user.cart.all()
        result = {}
        for recipe in recipes:
            ingredient = recipe.recipe.ingredients.values('parametrs_id',
                                                          'amount')
            for item in ingredient:
                parametrs_id, amount = item['parametrs_id'], item['amount']
                if parametrs_id in result:
                    result[parametrs_id] += amount
                else:
                    result[parametrs_id] = amount

        ingredients = []
        for parametrs_id, amount in result.items():
            ingredient = Ingredient.objects.get(id=parametrs_id)
            current_ingredient = {'name': ingredient.name,
                                  'amount': amount,
                                  'unit': ingredient.measurement_unit}
            ingredients.append(current_ingredient)

        file_pdf = PDF().creaete_list_ingredients(ingredients,)
        return FileResponse(io.BytesIO(file_pdf),
                            as_attachment=True,
                            filename="ingredients.pdf")
