"""
Django URL configuration for invitation management.

This module defines URL patterns for invitation-related views including
creation via API and HTML forms.
"""
from django.urls import path
from invitations.views import InvitationCreateAPIView, InvitationCreateView


urlpatterns =[
    path('create/', InvitationCreateAPIView.as_view(), name='invitation-create'),
    path('invite/', InvitationCreateView.as_view(), name='invite-voter'),
]