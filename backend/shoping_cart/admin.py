from django.contrib import admin

from shoping_cart.models import CartRecipes, ShopingCart


class CartRecipesInline(admin.TabularInline):
    model = CartRecipes


class ShopingCartAdmin(admin.ModelAdmin):
    inlines = (CartRecipesInline, )
    list_display = ('id', 'user', 'get_recipes')
    list_display_links = ('id', 'user', 'get_recipes')

    def get_recipes(self, cart):
        recipes = cart.recipes.all()
        print(type(recipes))
        result = ', '.join(
            [recipe.recipe.name for recipe in recipes[:3]])
        if recipes.count() > 3:
            result += f' и еще {recipes.count() - 3}'
        return result
    get_recipes.short_description = 'Рецепты'


admin.site.register(ShopingCart, ShopingCartAdmin)
