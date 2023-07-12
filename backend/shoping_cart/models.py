from django.db import models
from django.conf import settings

from recipes.models import Recipe


class ShopingCart(models.Model):
    """Модель Списка покупок."""
    class Meta:
        verbose_name = 'Корзина 2'
        verbose_name_plural = 'Корзина 2'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shoping_cart',
        verbose_name='Пользователь',
    )


class CartRecipes(models.Model):
    """Рецепты в конкретной корзине."""
    class Meta:
        verbose_name = 'Рецепт в корзине'
        verbose_name_plural = 'Рецепты в корзине'
        constraints = [
            models.UniqueConstraint(
                fields=['shoping_cart', 'recipe'],
                name='unique_shoping_cart_recipe',
            )
        ]

    shoping_cart = models.ForeignKey(ShopingCart,
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Корзина',
                               help_text='Рецепты в корзине',)

    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Рецепт',
                               help_text='Выбор рецепт',)