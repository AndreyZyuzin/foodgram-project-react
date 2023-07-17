from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CustomUserViewSet, IngredientViewSet, RecipeViewSet,
                       SubscriptionViewSet, TagViewSet)

v1_router = DefaultRouter()
v1_router.register('tags', TagViewSet, basename='tag')
v1_router.register('ingredients', IngredientViewSet, basename='ingredient')
v1_router.register('recipes', RecipeViewSet, basename='recipe')


CustomUserList = CustomUserViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

CustomUserAction = SubscriptionViewSet.as_view({
   'get': 'subscriptions',
   'post': 'subscribe',
   'delete': 'subscribe',   
})

urlpatterns = [
    path('users/', CustomUserList, name='users-list'),
    path('users/subscriptions/', CustomUserAction),
    path('users/<int:author_id>/subscribe/', CustomUserAction),
    path('', include(v1_router.urls)),
    path('', include('users.urls')),
]
