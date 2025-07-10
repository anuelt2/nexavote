"""
Django URL configuration for user authentication and registration.

This module defines URL patterns for user-related views including
registration, login, logout, and voter management.
"""
from django.urls import path
from users.views import RegisterViaTokenHTMLView, LoginView, LogoutView

# app_name = "users_auth"

urlpatterns = [
    path('register/voter/', RegisterViaTokenHTMLView.as_view(), name='register-voter-html'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]