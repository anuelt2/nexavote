"""
Django URL configuration for invitation management.

This module defines URL patterns for invitation-related views creation
via HTML forms.
"""
from django.urls import path
from invitations.views import InvitationCreateView


app_name = 'invitations'

urlpatterns =[
    # Admin HTML invite form (to be mounted under /auth/)
    path('create/', InvitationCreateView.as_view(), name='create-invite'),
]