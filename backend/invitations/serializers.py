"""
"""
from rest_framework import serializers

from invitations.models import Invitation
from election_events.models import ElectionEvent


class InvitationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for Invitation model.
    """
    election_event = serializers.PrimaryKeyRelatedField(
        queryset=ElectionEvent.objects.all()
    )

    class Meta:
        model = Invitation
        fields = ['email', 'election_event']
    
    def validate_email(self, value):
        """
        Custom validation for Invitation email field
        """
        if Invitation.objects.filter(email=value, is_used=False).exists():
            raise serializers.ValidationError("An active invitation already exists for this email")
        return value