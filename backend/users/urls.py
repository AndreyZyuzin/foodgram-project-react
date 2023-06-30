from django.urls import include, path


urlpatterns = [
    # path('auth/signup/', SignUpView.as_view(), name='user_create'),
    # path('auth/token/', TokenReceiveView.as_view(), name='token_receive'),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
