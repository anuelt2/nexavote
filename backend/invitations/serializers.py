"""
Django REST Framework serializers for invitation management.

This module contains serializers for handling invitation creation, listing,
and CSV upload functionality with comprehensive validation.
"""
from rest_framework import serializers

from election_events.models import ElectionEvent
from invitations.models import Invitation


class InvitationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new voter invitations.
    
    Handles the creation of invitation instances with validation for
    active election events and duplicate invitation prevention.
    
    Attributes:
        election_event: PrimaryKeyRelatedField for selecting election events
    """
    election_event = serializers.PrimaryKeyRelatedField(
        queryset=ElectionEvent.objects.all(),
        help_text="ID of the election event for this invitation"
    )

    class Meta:
        model = Invitation
        fields = ['email', 'election_event']
    
    def validate(self, data):
        """
        Validate election event status and prevent duplicate invitations.
        
        Ensures that invitations are only created for active election events
        and prevents duplicate unused invitations for the same email/event combination.
        
        Args:
            data (dict): Dictionary containing email and election_event
            
        Returns:
            dict: Validated data
            
        Raises:
            ValidationError: If election event is inactive or duplicate invitation exists
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
    Serializer for listing and retrieving invitation details.
    
    Provides read-only access to invitation information including
    automatically generated fields like token and timestamps.
    
    Fields:
        id: Invitation unique identifier
        email: Invited user's email address
        token: Invitation token (read-only)
        is_used: Boolean indicating if invitation was used (read-only)
        election_event: Associated election event ID
        created_at: Invitation creation timestamp (read-only)
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


class CSVUploadSerializer(serializers.Serializer):
    """
    Serializer for handling CSV file uploads for bulk invitation creation.
    
    Processes CSV files containing email addresses for bulk invitation
    generation and sending.
    
    Attributes:
        file (FileField): CSV file containing email addresses
        election_event_id (UUIDField): Election event ID for the invitations
    """
    file = serializers.FileField(
        help_text="CSV file containing email addresses for bulk invitations"
    )
    election_event_id = serializers.UUIDField(
        help_text="UUID of the election event for these invitations"
    )

    def validate_file(self, file):
        """
        Validate that the uploaded file is a CSV format.
        
        Args:
            file: The uploaded file object
            
        Returns:
            File: The validated file object
            
        Raises:
            ValidationError: If file is not in CSV format
        """
        if not file.name.endswith('.csv'):
            raise serializers.ValidationError('Only CSV files are allowed.')
        return file
