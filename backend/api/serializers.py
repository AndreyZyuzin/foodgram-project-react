from rest_framework import serializers
from djoser.serializers import UserSerializer, UserCreateSerializer

from users.models import CustomUser
from recipes.models import Tag




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

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'password'
                  )
        model = CustomUser



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag