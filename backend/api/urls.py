from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TagViewSet


v1_router = DefaultRouter()
# v1_router.register('users', UserViewSet, basename='user')
v1_router.register('tags', TagViewSet, basename='tag')


urlpatterns = [
    path('', include(v1_router.urls)),
    path('', include('users.urls')),
]
