"""
"""
from django.contrib import admin
from invitations.models import Invitation


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    """
    """
    list_display = ('email', 'election_event', 'is_used', 'created_at')
    search_fields = ('email',)