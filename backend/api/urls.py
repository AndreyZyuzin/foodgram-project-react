from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
# from recipes import ()


v1_router = DefaultRouter()
# v1_router.register('categories', CategoryViewSet, basename='category')


urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
