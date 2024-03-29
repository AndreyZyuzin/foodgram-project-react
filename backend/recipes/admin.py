from django.contrib import admin

from recipes.models import (AmountIngredient, Cart, Favorite, Ingredient,
                            Recipe, Tag)


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    search_fields = ('slug', 'name',)
    ordering = ('id', 'name', 'slug')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_display_links = ('id', 'name', 'measurement_unit')
    search_fields = ('name', )
    list_filter = ('measurement_unit',)
    ordering = ('id', 'name', 'measurement_unit')


class AmountIngredientInline(admin.TabularInline):
    model = AmountIngredient


class RecipeAdmin(admin.ModelAdmin):
    inlines = (AmountIngredientInline, )
    list_display = ('id',
                    'name',
                    'user',
                    'text',
                    'get_tag',
                    'get_ingredients',
                    'cooking_time',
                    )
    list_display_links = ('id', 'user', 'text', 'get_tag', 'get_ingredients')
    list_editable = ('name', 'cooking_time')
    search_fields = ('name', )
    list_filter = ('user', 'tags')
    # raw_id_fields = ('tags', 'ingredients')

    def get_tag(self, recipe):
        return ', '.join([tag.name for tag in recipe.tags.all()])
    get_tag.short_description = 'Теги'

    def get_ingredients(self, recipe):
        ingredients = recipe.ingredients.all()
        result = ', '.join(
            [ingredient.parametrs.name for ingredient in ingredients[:3]])
        if ingredients.count() > 3:
            result += f' и еще {ingredients.count() - 3}'
        return result
    get_ingredients.short_description = 'Ингредиенты'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_editable = ('user', 'recipe')


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)

admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Cart, CartAdmin)
