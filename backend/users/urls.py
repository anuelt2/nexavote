"""
Django URL configuration for user authentication and registration.

This module defines URL patterns for user-related views including
registration, login, logout, and voter management.
"""
from django.urls import path
# from django.contrib.auth.views import LoginView, LogoutView

from users.views import (
    RegisterViaTokenView,
    RegisterViaTokenHTMLView,
    LogoutAnyMethodView,
    AdminStaffRegistrationView,
    VoterListView, CustomLoginView
)

urlpatterns = [
    # API routes
    path('register/voter/', RegisterViaTokenView.as_view(), name='register-via-token'),
    # path('register/admin-staff/', AdminStaffRegistrationView.as_view(), name='register-admin-staff'),
    
    # HTML templates routes
    path('register/voter/html/', RegisterViaTokenHTMLView.as_view(), name='register-voter-html'),
    path('custom-login/', CustomLoginView.as_view(), name='custom-login'),
    path('custom-logout/', LogoutAnyMethodView.as_view(), name='custom-logout'),
    path('voters/', VoterListView.as_view(), name='voter-list'),
]