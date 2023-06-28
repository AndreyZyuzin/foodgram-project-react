from django.urls import path

from api.views import SignUpView, TokenReceiveView


urlpatterns = [
    path('auth/signup/', SignUpView.as_view(), name='user_create'),
    path('auth/token/', TokenReceiveView.as_view(), name='token_receive'),
]
