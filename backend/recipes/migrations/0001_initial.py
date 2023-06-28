# Generated by Django 4.2.2 on 2023-06-28 02:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название ингредиента', max_length=200, verbose_name='Название')),
                ('amount', models.IntegerField(help_text='Количество ингредиентов', verbose_name='Количество')),
                ('measurement_unit', models.CharField(help_text='Единица измерения', max_length=40, verbose_name='Единица')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название тега', max_length=200, unique=True, verbose_name='Название')),
                ('color', models.CharField(blank=True, help_text='Цвет в HEX', max_length=7, null=True, validators=[django.core.validators.RegexValidator(message='должен быть цвет в виде #fff или #ffffff', regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')], verbose_name='Цвет')),
                ('slug', models.SlugField(help_text='Уникальная строка тега', max_length=200, unique=True, verbose_name='Уникальная строка-индификатор')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название рецепта', max_length=200, verbose_name='Название')),
                ('image', models.ImageField(default=None, help_text='Ссылка рисунка', null=True, upload_to='images/', verbose_name='Рисунок')),
                ('text', models.TextField()),
                ('cooking_time', models.IntegerField(help_text='Время готовки в минутах', verbose_name='Время готовки')),
                ('ingredients', models.ManyToManyField(help_text='Ингредиенты рецепта', to='recipes.ingredient', verbose_name='Ингредиент')),
                ('tags', models.ManyToManyField(help_text='Тег', to='recipes.tag', verbose_name='Тег')),
            ],
        ),
    ]
