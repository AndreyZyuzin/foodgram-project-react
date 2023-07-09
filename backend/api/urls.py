from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSet, TagViewSet, CustomUserViewSet,
                    RecipeViewSet, SubscriptionViewSet)


v1_router = DefaultRouter()
v1_router.register('tags', TagViewSet, basename='tag')
v1_router.register('ingredients', IngredientViewSet, basename='ingredient')
v1_router.register('recipes', RecipeViewSet, basename='recipe')


#v1_router.register('users', CustomUserViewSet, basename='user')
#v1_router.register(
#    r'users/(?P<user_id>[\d]+)/subscribe',
#    CustomUserViewSet,
#    basename='subscribe'
#)



customUser_list = CustomUserViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

customUser_action = SubscriptionViewSet.as_view({
   'get': 'subscriptions',
   'post': 'subscribe',
   'delete': 'subscribe',   
})

urlpatterns = [
    path('users/', customUser_list, name='users-list'),
    path('users/subscriptions/', customUser_action),
    path('users/<int:user_id>/subscribe/', customUser_action),
    path('', include(v1_router.urls)),
    path('', include('users.urls')),
]
