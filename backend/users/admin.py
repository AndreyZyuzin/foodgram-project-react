from django.contrib import admin
from django.conf import settings


from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'first_name', 'last_name')



admin.site.register(CustomUser, CustomUserAdmin)
