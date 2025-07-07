"""
Django REST Framework serializers for invitation management.

This module contains serializers for handling invitation creation
with validation for election events and email addresses.
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
    
    def validate(self, data):
        """
        Validation for election_event is_active status
        """
        event = data.get('election_event')
        if not event.is_active:
            raise serializers.ValidationError("The selected election event is not active")
        return data
    
    def validate_email(self, value):
        """
        Custom validation for Invitation email field
        """
        if Invitation.objects.filter(email=value, is_used=False).exists():
            raise serializers.ValidationError("An active invitation already exists for this email")
        return value