from django.contrib import admin

from .models import Cart, Favorite, Ingredient, Recipe, Subscription, Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    search_fields = ('slug', 'name')
    ordering = ('pk', 'name', 'slug')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'amount', 'measurement_unit')
    search_fields = ('name', )
    ordering = ('pk', 'name')
    

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'name',
                    'image',
                    'text',
                    'get_tag',
                    'get_ingredient',
                    'cooking_time',)
    # search_fields = ('name', 'tag__name', 'ingredient__name')
    # ordering = ('name', 'tag__name', 'ingredient__name')
    # raw_id_fields = ('tags', 'ingredients')
    

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'following')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'ingredient')


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Cart, CartAdmin)
