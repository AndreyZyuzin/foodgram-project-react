from django.contrib import admin

from .models import Ingredient, Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    search_fields = ('slug', 'name')
    ordering = ('pk', 'name', 'slug')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'amount', 'measurement_unit')
    search_fields = ('name', )
    ordering = ('pk', 'name')
    
    






admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
