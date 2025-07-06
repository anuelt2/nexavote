"""
"""
from django.contrib import admin

from users.models import User, VoterProfile
from users.utils import send_password_reset_email


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
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
        """
        super().save_model(request, obj, form, change)

        role = form.cleaned_data.get("role")

        if not change and obj.role in ['admin', 'staff']:
            print("Sending password reset email...")
            send_password_reset_email(request, obj)


@admin.register(VoterProfile)
class VoterProfileAdmin(admin.ModelAdmin):
    """
    """
    list_display = ('user', 'election_event')