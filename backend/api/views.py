from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from djoser.permissions import CurrentUserOrAdmin


from recipes.models import IngredientParam, Tag
from users.models import CustomUser
from .serializers import (CustomUserCreateSerializer, CustomUserSerializer,
                          IngredientParamSerializer, TagSerializer)
from .pagination import CustomUsersPagination
from .permissions import PermissionsForUsers, isAdmin


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    # serializer_class = CustomUserSerializer
    pagination_class = CustomUsersPagination
    permission_classes = (PermissionsForUsers,)
    http_method_names = ['get', 'post']
    serializer_action_classes = {
        'list': CustomUserSerializer,
        'create': CustomUserCreateSerializer,
    }

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'GET':
            return CustomUserSerializer
        return CustomUserCreateSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ['get']
    permission_classes = (isAdmin, )


class IngredientParamViewSet(viewsets.ModelViewSet):
    queryset = IngredientParam.objects.all()
    serializer_class = IngredientParamSerializer
    http_method_names = ['get']
    permission_classes = (isAdmin, )
