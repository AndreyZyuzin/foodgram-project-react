from django.contrib import admin

from .models import CustomUser


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
    )
    list_editable = ('role',)
    search_fields = ('username',)
    empty_value_display = '-пусто-'


admin.site.register(CustomUser, UserAdmin)
