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

from drf_yasg.views import get_schema_view  # type: ignore
from drf_yasg import openapi    # type: ignore
from rest_framework import permissions

from core.views import api_root, HomeView


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

    # Authentication and Password Reset (Template/UI)
    path('auth/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('auth/', include('django.contrib.auth.urls')),
    path('auth/', include('users.urls_auth')),
    path('auth/invitation/', include('invitations.urls')),

    # Other Template Views
    path('', HomeView.as_view(), name='home'),
    path('', include('users.urls')),
    path('events/', include('election_events.urls')),
    path('', include('elections.urls')),

     # API Root
    path('api/', api_root, name='api-root'),

    # API Authentication (DRF Browsable API login/logout)
    path('api-auth/', include('rest_framework.urls')),

    # API Endpoints By App
    path('api/users/', include(('users.urls_api', 'users_api'), namespace='users_api')),
    path('api/invitation/', include('invitations.urls_api')),
    path('api/events/', include(('election_events.urls_api', 'events_api'), namespace='events_api')),
    path('api/', include('elections.urls_api')),
    path('api/votes/', include('votes.urls')),
    
    # API documentation (Swagger / Redoc)
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
