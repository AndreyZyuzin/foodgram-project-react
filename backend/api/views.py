import io

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly, IsAdminUser)
from djoser.permissions import CurrentUserOrAdmin
from django.shortcuts import get_object_or_404
from django.http import FileResponse



from recipes.models import Cart, Favorite, Ingredient, Tag, Recipe
from users.models import CustomUser, Subscription
from .serializers import (CustomUserCreateSerializer, CustomUserSerializer,
                          IngredientSerializer,
                          RecipeSerializer, RecipeShortSerializer,
                          TagSerializer, SubscriptionSerializer,)
from .pagination import (CustomUsersPagination, SubscriptionPagination,
                         RecipesPagination)
from .permissions import isAuthor, isAuthorOrReadOnly
from core.utilites.pdf import PDF


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
            user=author, following__id=user_id).exists()
        if request.method=='POST' and not is_subscription:
            user = CustomUser.objects.get(pk=user_id)
            subscription = Subscription.objects.create(
                user=author, following=user)
            logger.debug(f'id::{id}')
            serializer = SubscriptionSerializer(
                Subscription.objects.get(id=subscription.id))
            return Response(serializer.data)
        if request.method=='DELETE' and is_subscription:
            Subscription.objects.get(
                user=author, following__id=user_id).delete()
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


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('-pub_date')
    serializer_class = RecipeSerializer
    permission_classes = (isAuthorOrReadOnly,)
    pagination_class = RecipesPagination


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    @action(detail=True,
            methods=['POST', 'DELETE'],
            permission_classes=(IsAuthenticated,))
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
            return Response()
            
        return Response('осталось как было')


    @action(detail=True,
            methods=['POST', 'DELETE'],
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk=None):
        """Добавление и удаление рецепта pk в корзину."""
        logger.debug(f'!!!!!!!!!! shopping_cart !!!!!!!!!')
        logger.debug(f'favorite:\nself:{self}\nrequest:{request}\npk:{pk}')
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
        from django.db.models import Count, Sum
        user = request.user
        recipes = user.cart.all()
        for recipe in recipes:
            logging.debug(f'recipe: {recipe.recipe.ingredients.values()}')
        # annotated_results = user.cart.annotation(ingredient_sum = Count(recipe.ingredients))
        logging.debug(f'1: {recipes}')
        logging.debug(f"2: {recipes.values('recipe_id').annotate(Count('recipe__ingredients__parametrs'))}")
        logging.debug(f"3: {recipes.values('recipe_id').annotate(Sum('recipe__ingredients__amount'))}")
        logging.debug(f"4: {recipes.values('recipe_id').annotate()}")
        
        result = {}
        for recipe in recipes:
            ingredient = recipe.recipe.ingredients.values('parametrs_id',
                                                          'amount')
            logging.debug(f'tmp: {ingredient}')
            for item in ingredient:
                parametrs_id, amount = item['parametrs_id'], item['amount']
                if parametrs_id in result:
                    result[parametrs_id] += amount
                else:
                    result[parametrs_id] = amount
        logging.debug(f'result: {result}')

        ingredients = []
        for parametrs_id, amount in result.items():
            ingredient = Ingredient.objects.get(id=parametrs_id)
            logging.debug(f'ingredient: {ingredient}, {ingredient.name}, {ingredient.measurement_unit}')
            current_ingredient = {'name': ingredient.name,
                                  'amount': amount,
                                  'unit': ingredient.measurement_unit}
            ingredients.append(current_ingredient)
        logging.debug(f'ingredients: {ingredients}, {type(ingredients)}')
        
        file_pdf = PDF().creaete_list_ingredients(ingredients,)
        response = FileResponse(io.BytesIO(file_pdf),
                                as_attachment=True,
                                filename="ingredients.pdf")
        return response

