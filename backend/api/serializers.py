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
    tags = TagSerializer(many=True,)
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
        if not user.is_authenticated:
            return False
        return Favorite.objects.filter(user=user, recipe=recipe).exists()

    def get_is_in_shopping_cart(self, obj):
        """Проверка, что рецепт в корзине."""
        logger.debug('get_is_in_shopping_cart')
        return True  

    def create(self, validated_data):
        logger.debug(f'validated_data: {validated_data}')
        tags = validated_data.pop('tags')
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
        # logger.debug(f'self: {self}')
        logger.debug(f'instance: {instance}')
        logger.debug(f'instance.tags: {instance.tags.all().values()}')
        logger.debug(f'instance.ingredients: {instance.ingredients.all().values()}')
        logger.debug(f'validated_data: {validated_data}')
        
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
                logger.debug(f'ingredient: {ingredient} {type(ingredient)}')
                
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


    def to_internal_value(self, data):
        logger.debug('to_internal_value')
        return data



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
            user=obj.following, following=obj.user).exists()

    def get_recipes(self, obj):
        logging.debug(f'get_recipes {obj}')
        recipes = Recipe.objects.filter(user=obj.following)
        logging.debug(f'{recipes}')
        serializers = RecipeShortSerializer(recipes, many=True)
        return serializers.data


    def get_recipes_count(self,obj):
        recipes = Recipe.objects.filter(user=obj.following)
        return recipes.count()



