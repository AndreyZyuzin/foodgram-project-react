from rest_framework.pagination import PageNumberPagination


class CustomUsersPagination(PageNumberPagination):
    page_size = 3

class SubscriptionPagination(PageNumberPagination):
    page_size = 2