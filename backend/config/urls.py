"""
NexaVote Application URL Configuration

This module defines the main URL routing for NexaVote application.
It includes routes for authentication, API endpoints, admin interface,
and API documentation.

URL Structures:
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from core.views import api_root, HomeView


urlpatterns = [
    # Admin Interface
    path('admin/', admin.site.urls),

    path('auth/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('auth/', include('django.contrib.auth.urls')),

    # API login/logout
    path('api-auth/', include('rest_framework.urls')),

    # API Root
    path('api/', api_root, name='api-root'),

    # User API Endpoints
    # path('api/users/', include('users.urls')),
    path('api/invitations/', include('invitations.urls')),

    #Vote API
    path('api/votes/', include('votes.urls')),

    # Election Events API Endpoints
    # path('api/election-events/', include('election_events.urls')),
    path('api/', include('elections.urls')),

    # HTML UI (Templates)
    path('', HomeView.as_view(), name='home'),
    path('auth/', include('users.urls')),
    path('auth/', include('election_events.urls')),
    path('auth/', include('elections.urls')),
]
