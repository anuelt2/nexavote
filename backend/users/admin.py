"""
Django admin configuration for user models.

This module defines admin interfaces for User and VoterProfile models
with custom display options and actions.
"""
from django.contrib import admin
from users.models import User, VoterProfile
from users.utils import send_password_reset_email


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Admin interface for User model with custom display and actions.
    """
    list_display = (
        'email',
        'first_name',
        'last_name',
        'role',
        'is_active',
        'is_staff',
        'created_at'
    )
    search_fields = (
        'email',
        'first_name',
        'last_name'
    )
    
    def save_model(self, request, obj, form, change):
        """
        Override save_model to send password reset email for new admin/staff users.
        
        Args:
            request: The HTTP request object
            obj: The model instance being saved
            form: The form instance
            change: Boolean indicating if this is a change (True) or add (False)
        """
        super().save_model(request, obj, form, change)
        role = form.cleaned_data.get("role")
        
        if not change and obj.role in ['admin', 'staff']:
            print("Sending password reset email...")
            send_password_reset_email(request, obj)


@admin.register(VoterProfile)
class VoterProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for VoterProfile model with user and election event display.
    """
    list_display = ('user', 'election_event')
