"""
"""
from django.contrib import admin

from invitations.models import Invitation
from invitations.views import InvitationCreateAPIView


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    """
    Admin config for managing invitations and sending invite email on creation.
    """
    list_display = ('email', 'election_event', 'is_used', 'created_at')
    search_fields = ('email',)

    def save_model(self, request, obj, form, change):
        """
        """
        is_new = obj.pk is None
        super().save_model(request, obj, form, change)
        if is_new:
            view = InvitationCreateAPIView()
            view.request = request
            view.send_invite_email(obj)