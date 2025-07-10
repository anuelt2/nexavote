"""
Django admin configuration for invitation management.

This module provides admin interface customization for the Invitation model,
including automatic email sending when invitations are created through the admin.
"""
from django.contrib import admin

from invitations.models import Invitation
from invitations.views import InvitationCreateAPIView


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    """
    Django admin configuration for managing invitations.
    
    Provides a customized admin interface for creating and managing voter invitations
    with automatic email sending functionality when new invitations are created.
    
    Attributes:
        list_display: Fields to display in the admin list view
        search_fields: Fields to enable searching in the admin interface
    """
    list_display = ('email', 'election_event', 'is_used', 'created_at')
    search_fields = ('email',)

    def save_model(self, request, obj, form, change):
        """
        Override save_model to send invitation emails for new invitations.
        
        Automatically sends invitation emails when new invitations are created
        through the Django admin interface.
        
        Args:
            request: The HTTP request object
            obj: The Invitation model instance being saved
            form: The admin form instance
            change: Boolean indicating if this is an update (True) or creation (False)
        """
        is_new = obj.pk is None
        super().save_model(request, obj, form, change)
        if is_new:
            view = InvitationCreateAPIView()
            view.request = request
            view.send_invite_email(obj)

