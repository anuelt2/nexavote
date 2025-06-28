"""
"""
from django.contrib import admin
from users.models import User, VoterProfile


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


@admin.register(VoterProfile)
class VoterProfileAdmin(admin.ModelAdmin):
    """
    """
    list_display = ('user', 'election_event')