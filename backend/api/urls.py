from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProfileViewSet

v1_router = DefaultRouter()
# v1_router.register('categories', CategoryViewSet, basename='category')
v1_router.register('users', ProfileViewSet, basename='users')


urlpatterns = [
    path('', include(v1_router.urls)),
    path('', include('users.urls'))
]
