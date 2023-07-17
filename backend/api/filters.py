import logging

import django_filters
from recipes.models import Cart, Favorite, Recipe, Tag
from users.models import CustomUser

logger = logging.getLogger(__name__)


BOOLEAN_CHOICES = ((1, True), (0, False))


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='istartswith')


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all())
    author = django_filters.ModelChoiceFilter(
        field_name='user',
        queryset=CustomUser.objects.all(),)
    is_favorited = django_filters.NumberFilter(
        field_name='is_favorited',
        method='get_is_favorited',
    )
    is_in_shopping_cart = django_filters.NumberFilter(
        method='get_is_in_shopping_cart',)

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if user.is_anonymous:
            return queryset
        if not value:
            return queryset
        favorites = Favorite.objects.filter(user=user)
        return queryset.filter(favorites__in=favorites)

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if user.is_anonymous:
            return queryset
        if not value:
            return queryset
        cart = Cart.objects.filter(user=user)
        return queryset.filter(cart__in=cart)

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')
