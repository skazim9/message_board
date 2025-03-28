from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.apps import UsersConfig
from users.views import UserCreateAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('users/reset_password/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('users/reset_password_confirm/', views.ResetPasswordConfirmView.as_view(), name='reset_password_confirm'),
]
