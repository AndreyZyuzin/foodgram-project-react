from rest_framework import serializers
from django.core.validators import RegexValidator
from rest_framework.validators import UniqueValidator

from users.models import CustomUser


class SignUpSerializer(serializers.Serializer):
    """Cериализатор для регистрации пользователя."""
    email = serializers.EmailField(
        required=True,
        max_length=254,
    )
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+',
                message='Неподходящий формат имени пользователя'), ])
    first_name = serializers.CharField(
        max_length=150,
        required=False)
    last_name = serializers.CharField(
        max_length=150,
        required=False)
    role = serializers.CharField(
        required=False)
    bio = serializers.CharField(
        required=False)

    class Meta:
        fields = '__all__'
        model = CustomUser

    def validate(self, attrs):
        if attrs.get('username') == 'me':
            raise serializers.ValidationError(
                'Запрещено использовать юзернейм "me"')
        return attrs

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.role = validated_data.get('role', instance.role)
        if instance.role not in ('user', 'moderator', 'admin'):
            raise serializers.ValidationError()
        instance.save()
        return instance


class ProfileSerializer(SignUpSerializer):
    """Cериализатор для работы с пользователем."""
    email = serializers.EmailField(
        required=True,
        max_length=254,
        validators=[UniqueValidator(queryset=CustomUser.objects.all()), ]
    )
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+',
                message='Неподходящий формат имени пользователя'),
            UniqueValidator(queryset=CustomUser.objects.all()), ]
    )

    class Meta:
        fields = '__all__'
        model = CustomUser


class UserMeSerializer(serializers.ModelSerializer):
    """Cериализатор для работы с эндпоинтом /me/."""
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+',
                message='Неподходящий формат имени пользователя'),
            UniqueValidator(queryset=CustomUser.objects.all()), ])

    class Meta:
        fields = '__all__'
        model = CustomUser
        read_only_fields = ['role']


class TokenReceiveSerializer(serializers.Serializer):
    """Cериализатор для работы с токеном."""
    username = serializers.CharField(
        required=True,
        max_length=150, )
    confirmation_code = serializers.CharField(
        required=True, )

    class Meta:
        fields = '__all__'
        model = CustomUser