# Generated by Django 4.2.2 on 2023-07-12 03:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
        ('shoping_cart', '0002_alter_cartrecipes_recipe_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartrecipes',
            name='recipe',
            field=models.ForeignKey(help_text='Выбор рецепт', on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to='recipes.recipe', verbose_name='Рецепт'),
        ),
    ]
