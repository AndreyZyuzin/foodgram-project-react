from django.contrib import admin
from django.conf import settings


from .models import CustomUser, Subscription


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email')


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'following')
    list_editable = ('author', 'following')
    


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)