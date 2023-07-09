from rest_framework.pagination import PageNumberPagination


class CustomUsersPagination(PageNumberPagination):
    page_size = 6

class SubscriptionPagination(PageNumberPagination):
    page_size = 6

class RecipesPagination(PageNumberPagination):
    page_size = 6