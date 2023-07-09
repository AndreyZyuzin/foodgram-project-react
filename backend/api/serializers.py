import base64

from rest_framework import serializers
from djoser.serializers import UserSerializer, UserCreateSerializer
from django.core.files.base import ContentFile

from users.models import (CustomUser, Subscription)
from recipes.models import (AmountIngredient, Favorite, Ingredient, Recipe,
                            Tag)

import logging
logger = logging.getLogger(__name__)


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed',
                  )
        model = CustomUser

    def get_is_subscribed(self, obj):
        """Проверка является пользователь подписчиком автора."""
        return True

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'password'
                  )
        model = CustomUser


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')

class AmountIngredientSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'amount', 'measurement_unit')
        model = AmountIngredient

    def get_name(self, obj):
        return obj.parametrs.name
    
    def get_measurement_unit(self, obj):
        return obj.parametrs.measurement_unit


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')  
            ext = format.split('/')[-1]  
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True,) # read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = AmountIngredientSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
            )

    def get_is_favorited(self, obj):
        """Проверка является пользователь данный рецепт внес в желания."""
        return True

    def get_is_in_shopping_cart(self, obj):
        """Проверка, что рецепт в корзине."""
        logger.debug('get_is_in_shopping_cart')
        return True  

    def create(self, valdated_data):
        logger.debug('RecipeSerializer.create')
        tags = valdated_data.pop('tags')
        ingredients = valdated_data.pop('ingredients')
        recipe = Recipe.objects.create(**valdated_data)
        for tag in tags:
            current_tag, status = Tag.objects.get_or_create(**tag)
            Recipe.tags.through.objects.create(tags=current_tag, recipe=recipe)


class RecipeShortSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)

    
class SubscriptionSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="following.email")
    id = serializers.EmailField(source="following.id")
    username = serializers.EmailField(source="following.username")
    first_name = serializers.EmailField(source="following.first_name")
    last_name = serializers.EmailField(source="following.last_name")
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed',
                  'recipes',
                  'recipes_count',
                  )

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(
            author=obj.following, following=obj.author).exists()

    def get_recipes(self, obj):
        logging.debug(f'get_recipes {obj}')
        recipes = Recipe.objects.filter(author=obj.following)
        logging.debug(f'{recipes}')
        serializers = RecipeShortSerializer(recipes, many=True)
        return serializers.data


    def get_recipes_count(self,obj):
        recipes = Recipe.objects.filter(author=obj.following)
        return recipes.count()


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('id', 'recipe', 'user')




