"""
NexaVote Application URL Configuration

This module defines the main URL routing for NexaVote application.
It includes routes for authentication, API endpoints, admin interface,
and API documentation.

URL Structures:
"""
from django.contrib import admin
from django.urls import path, include
from core.views import api_root

urlpatterns = [
    # Admin Interface
    path('admin/', admin.site.urls),

    # API Root
    path('', api_root, name='home'),

    # User API Endpoints
    path('api/users/', include('users.urls')),
    path('api/invitations/', include('invitations.urls')),
]
