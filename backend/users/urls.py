"""
Django URL configuration for authenticated user-facing pages.

This module defines URL patterns for user-related views including
registration, login, logout, and voter management.
"""
from django.urls import path
from users.views import VoterListView

urlpatterns = [
    path('voters/', VoterListView.as_view(), name='voter-list'),
]