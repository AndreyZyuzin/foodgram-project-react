import secrets

from django.conf import settings
from django.core.mail import send_mail
from rest_framework import generics, status, filters, viewsets
from rest_framework.decorators import action
from django.db import IntegrityError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import CustomUser
from .serializers import (ProfileSerializer, SignUpSerializer,
                          TokenReceiveSerializer, UserMeSerializer)


class SignUpView(generics.CreateAPIView):

    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        try:
            user, _ = CustomUser.objects.get_or_create(
                username=username,
                email=email)
        except IntegrityError:
            return Response(
                'Данный e-mail или username уже используется!',
                status=status.HTTP_400_BAD_REQUEST)

        confirmation_code = secrets.token_hex(32)
        user.confirmation_code = str(confirmation_code)
        user.save()

        send_mail(
            subject='Ваш код подтверждения',
            message=f'Ваш код для регистрации: {confirmation_code}',
            from_email=settings.DOMAIN_NAME,
            recipient_list=[email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenReceiveView(generics.CreateAPIView):

    def post(self, request, *args, **kwargs):
        serializer = TokenReceiveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            CustomUser,
            username=request.data.get('username')
        )
        refresh = RefreshToken.for_user(user)

        if user.confirmation_code != request.data.get('confirmation_code'):
            return Response(
                'Неверный код подтверждения',
                status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'token': str(refresh.access_token)
        }, status=status.HTTP_200_OK)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = ()
    serializer_class = ProfileSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_object(self):
        # Для GET запроса по юзернейму
        return get_object_or_404(CustomUser,
                                 username=self.kwargs.get('pk'))

    def create(self, request, *args, **kwargs):
        serializer = ProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomUser.objects.create(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'])

        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False,
            methods=('GET', 'PATCH'),
            permission_classes=())
    # Для работы с эндопоинтом /me/
    def me(self, request):
        if request.method == 'GET':
            user_info = get_object_or_404(CustomUser, username=request.user)
            serializer = self.get_serializer(user_info)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = UserMeSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
