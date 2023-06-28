from django.db import models
from django.core.validators import RegexValidator, MinValueValidator


class Tag(models.Model):
    """Модель тегов.
    
    По ТЗ name возможен быть не уникальным. Но возможно добавить unique=True.
    По ТЗ сolor не уточнено. Сделано на выбор 3-численные и 6-численные
    компоненты RGB.
    """
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
    # author
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
                                  help_text='Тег',)
    cooking_time = models.IntegerField(verbose_name='Время готовки',
                                       help_text='Время готовки в минутах', )