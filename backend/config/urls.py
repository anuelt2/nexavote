"""
NexaVote Application URL Configuration

This module defines the main URL routing for NexaVote application.
It includes routes for authentication, API endpoints, admin interface,
and API documentation.

URL Structures:
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include, re_path

from core.views import api_root, HomeView

from drf_yasg.views import get_schema_view  # type: ignore
from drf_yasg import openapi    # type: ignore
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="NexaVote API",
        default_version='v1',
        description="API documentation for NexaVote",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


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

    # Swagger Docs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
