"""
Django REST Framework serializers for invitation management.

This module contains serializers for handling invitation creation
with validation for election events and email addresses.
"""
from rest_framework import serializers

from election_events.models import ElectionEvent
from invitations.models import Invitation


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
        email = data.get('email')

        if not event.is_active:
            raise serializers.ValidationError("The selected election event is not active")
        
        if Invitation.objects.filter(email=email, election_event=event, is_used=False).exists():
            raise serializers.ValidationError(
                f"An unused invitation for {email} already exists for this election event."
            )
        
        return data


class InvitationListSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = Invitation
        fields = [
            'id',
            'email',
            'token',
            'is_used',
            'election_event',
            'created_at'
        ]
        read_only_fields = ['token', 'is_used', 'created_at']