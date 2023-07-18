from django.conf import settings
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils import timezone


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
            ), ],
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


class Recipe(models.Model):
    """Модель рецепта."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
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
    tags = models.ManyToManyField(Tag,
                                  verbose_name='Тег',
                                  help_text='Теги рецепта',
                                  db_index=True)
    cooking_time = models.IntegerField(
        verbose_name='Время готовки',
        help_text='Время готовки в минутах',
        validators=[
            MinValueValidator(
                limit_value=1,
                message='Время готовки должно быть положительным.'
            ), ]
    )
    pub_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата создания',
        help_text='Дата, когда был создан рецепт',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Часть модели ингредиентов."""
    name = models.CharField(max_length=200,
                            unique=True,
                            verbose_name='Название',
                            help_text='Название ингредиента',
                            db_index=True,)
    measurement_unit = models.CharField(max_length=40,
                                        verbose_name='Единица',
                                        help_text='Единица измерения', )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class AmountIngredient(models.Model):
    """Модель ингредиентов."""
    parametrs = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='params',
        verbose_name='Имя',
        help_text='Имя и размерность ингредиента',
    )
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='ingredients',
                               verbose_name='Ингредиент',
                               help_text='Ингредиенты рецепта',)
    amount = models.IntegerField(
        verbose_name='Количество',
        help_text='Количество ингредиентов',
        validators=[
            MinValueValidator(
                limit_value=0,
                message='Количество ингредиентов не должно быть отрицательным.'
            ), ]
    )

    class Meta:
        verbose_name = 'Кол-во ингредиентов'
        verbose_name_plural = 'Кол-во ингредиентов'

    def __str__(self):
        return (f'{self.parametrs.name} - '
                f'{self.amount} {self.parametrs.measurement_unit}')


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
        settings.AUTH_USER_MODEL,
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
                fields=['user', 'recipe'],
                name='unique_cart_user_recipe',
            )
        ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь',
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Рецепт',
    )
