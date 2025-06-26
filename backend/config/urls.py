"""
NexaVote Application URL Configuration

This module defines the main URL routing for NexaVote application.
It includes routes for authentication, API endpoints, admin interface,
and API documentation.

URL Structures:
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin Interface
    path('admin/', admin.site.urls),

    # User API Endpoints
    path('api/users/', include('users.urls'))
]
