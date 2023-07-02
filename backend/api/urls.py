from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientParamViewSet, TagViewSet, CustomUserViewSet


v1_router = DefaultRouter()
v1_router.register('tags', TagViewSet, basename='tag')
v1_router.register('ingredients', IngredientParamViewSet, basename='ingredient')

customUser_list = CustomUserViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

urlpatterns = [
    path('users/', customUser_list, name='users-list'),
    path('', include(v1_router.urls)),
    path('', include('users.urls')),
]
