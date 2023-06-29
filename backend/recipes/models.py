from django.db import models
from django.core.validators import RegexValidator, MinValueValidator

from users.models import CustomUser

class Tag(models.Model):
    """Модель тегов."""
    name = models.CharField(max_length=200,
                            unique=True,
                            verbose_name='Название',
                            help_text='Название тега', )
    color = models.CharField(
        max_length=7,
        blank=True,
        null=True,
        verbose_name='Цвет',
        help_text='Цвет в HEX',
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='должен быть цвет в виде #fff или #ffffff',
                ),],
        )
    slug = models.SlugField(max_length=200,
                            unique=True,
                            verbose_name='Уникальная строка-индификатор',
                            help_text='Уникальная строка тега', )

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиентов."""
    name = models.CharField(max_length=200,
                            unique=True,
                            verbose_name='Название',
                            help_text='Название ингредиента', )
    amount = models.IntegerField(
        verbose_name='Количество',
        help_text='Количество ингредиентов',
        validators=[
            MinValueValidator(
                limit_value=0,
                message='Количество ингредиентов не должно быть отрицательным.'
                ),]
        )
    measurement_unit = models.CharField(max_length=40,
                            verbose_name='Единица',
                            help_text='Единица измерения', )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецепта."""
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
        help_text='Автор рецепта',
    )
    name = models.CharField(max_length=200,
                            verbose_name='Название',
                            help_text='Название рецепта', )
    image = models.ImageField(upload_to='images/',
                              null=True,
                              default=None,
                              verbose_name='Рисунок',
                              help_text='Ссылка рисунка',)
    text = models.TextField()
    ingredients = models.ManyToManyField(Ingredient,
                                         verbose_name='Ингредиент',
                                         help_text='Ингредиенты рецепта',)
    tags = models.ManyToManyField(Tag,
                                  verbose_name='Тег',
                                  help_text='Теги рецепта',)
    cooking_time = models.IntegerField(verbose_name='Время готовки',
                                       help_text='Время готовки в минутах', )

    def get_tag(self):
        return ', '.join([tag.name for tag in self.tags.all()])

    get_tag.short_description = 'Теги'


    def get_ingredient(self):
        return ', '.join(
            [ingredient.name for ingredient in self.ingredients.all()])

    get_ingredient.short_description = 'Ингредиенты'
    
    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Subscription(models.Model):
    """Модель подписки."""
    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_following_user',
            )
        ]

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Автор',
        help_text='Автор',
    )

    following = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписчики',
        help_text='Подписчики',
    )


class Favorite(models.Model):
    """Модель избранное."""
    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe',
            )
        ]

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )


class Cart(models.Model):
    """Модель Списка покупок."""
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'ingredient'],
                name='unique_user_ingredient',
            )
        ]

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь',
    )

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Ингредиент',
    )