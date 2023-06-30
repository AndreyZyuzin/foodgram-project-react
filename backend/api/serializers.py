from rest_framework import serializers
from djoser.serializers import UserSerializer

from users.models import CustomUser



class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()
    
    class Meta:
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed',
                  )
        model = CustomUser

    def get_is_subscribed(self, obj):
        """Проверка является пользователь подписчиком автора."""
        return True