"""
Django URL configuration for user authentication and registration.

This module defines URL patterns for user-related API views.
"""
from django.urls import path
from users.views import (
    RegisterViaTokenView,
    LoginAPIView,
    LogoutAPIView,
    CurrentUserView,
    PasswordResetConfirmAPIView,
    PasswordResetRequestAPIView
)
app_name = "users_api"

urlpatterns = [
    path('register/voter/', RegisterViaTokenView.as_view(), name='register-via-token'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('me/', CurrentUserView.as_view(), name='current-user'),
    path('auth/reset-password/confirm/', PasswordResetConfirmAPIView.as_view(), name='password-reset-confirm'),
    path('password-reset/', PasswordResetRequestAPIView.as_view(), name='password-reset-request'),
]