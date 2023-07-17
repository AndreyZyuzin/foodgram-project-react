import base64
import logging

from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from recipes.models import (AmountIngredient, Cart, Favorite, Ingredient,
                            Recipe, Tag)
from users.models import CustomUser, Subscription

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
        request = self.context.get('request')
        user = request.user
        if user.is_anonymous:
            return False
        return Subscription.objects.filter(user=obj, following=user).exists()


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
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True, source='user')
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

    def get_is_favorited(self, recipe):
        """Проверка является пользователь данный рецепт внес в желания."""
        request = self.context.get('request')
        user = request.user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(user=user, recipe=recipe).exists()

    def get_is_in_shopping_cart(self, obj):
        """Проверка, что рецепт в корзине."""
        request = self.context.get('request')
        user = request.user
        if user.is_anonymous:
            return False
        return Cart.objects.filter(user=user, recipe=obj).exists()

    def create(self, validated_data):
        if 'tags' in self.initial_data:
            tags = self.initial_data.pop('tags')
        else:
            tags = validated_data.pop('tags')
        if 'ingredients' in self.initial_data:
            ingredients = self.initial_data.pop('ingredients')
        else:
            ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)

        for tag_id in tags:
            tag = Tag.objects.get(id=tag_id)
            Recipe.tags.through.objects.create(recipe=recipe, tag=tag)

        for current_ingredient in ingredients:
            current_ingredient_id = current_ingredient['id']
            ingredient = Ingredient.objects.get(id=current_ingredient_id)
            amount = current_ingredient['amount']
            AmountIngredient.objects.create(
                recipe=recipe, parametrs=ingredient, amount=amount)
        return recipe

    def update(self, instance: Recipe, validated_data):
        if 'tags' in validated_data:
            new_tags_ids = validated_data.pop('tags')
            old_tags = instance.tags.all()

            for current_tag in old_tags:
                if current_tag.id not in new_tags_ids:
                    instance.tags.through.objects.get(
                        recipe=instance, tag=current_tag
                    ).delete()

            for tag_id in new_tags_ids:
                tag = Tag.objects.get(id=tag_id)
                instance.tags.through.objects.update_or_create(
                    recipe=instance, tag=tag)

        if 'ingredients' in validated_data:
            new_ingredients = validated_data.pop('ingredients')
            old_ingredients = instance.ingredients.all()

            for ingredient in old_ingredients:
                AmountIngredient.objects.get(
                    recipe=instance, parametrs=ingredient.parametrs
                ).delete()

            for current_ingredient in new_ingredients:
                ingredient = Ingredient.objects.get(
                    id=current_ingredient['id'])
                AmountIngredient.objects.update_or_create(
                    recipe=instance, parametrs=ingredient,
                    defaults={'amount': current_ingredient['amount']}
                )

        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time',
                                                   instance.cooking_time)

        instance.save()

        return instance


class RecipeShortSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)


class SubscriptionSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email")
    id = serializers.EmailField(source="user.id")
    username = serializers.EmailField(source="user.username")
    first_name = serializers.EmailField(source="user.first_name")
    last_name = serializers.EmailField(source="user.last_name")
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
            user=obj.user, following=obj.following).exists()

    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(user=obj.user)
        serializers = RecipeShortSerializer(recipes, many=True)
        return serializers.data

    def get_recipes_count(self, obj):
        recipes = Recipe.objects.filter(user=obj.user)
        return recipes.count()
