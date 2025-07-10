"""
Django REST Framework serializers for election management.

This module defines serializers for Election and Candidate models,
handling validation and data transformation for election-related API endpoints.
"""
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from elections.models import Election, Candidate


class ElectionSerializer(serializers.ModelSerializer):
    """
    Serializer for Election model instances.
    
    Handles serialization and validation of election data including
    time validation against associated election events.
    
    Fields:
        id: Election unique identifier
        title: Election title
        description: Election description
        start_time: Election start timestamp
        end_time: Election end timestamp
        is_active: Boolean indicating if election is active
        election_event: Associated election event ID
        election_event_title: Election event title (read-only)
    """
    election_event_title = serializers.CharField(
        source='election_event.title', 
        read_only=True,
        help_text="Title of the associated election event"
    )

    class Meta:
        model = Election
        fields = [
            'id',
            'title',
            'description',
            'start_time',
            'end_time',
            'is_active',
            'election_event',
            'election_event_title'
        ]
        extra_kwargs = {
            'title': {'help_text': 'Title of the election'},
            'description': {'help_text': 'Detailed description of the election'},
            'start_time': {'help_text': 'Election start date and time'},
            'end_time': {'help_text': 'Election end date and time'},
            'is_active': {'help_text': 'Whether the election is currently active'},
            'election_event': {'help_text': 'ID of the associated election event'}
        }
    
    def validate(self, attrs):
        """
        Validate election timing against election event constraints.
        
        Ensures that election start/end times fall within the bounds
        of the associated election event timing.
        
        Args:
            attrs (dict): Dictionary of field values to validate
            
        Returns:
            dict: Validated attributes
            
        Raises:
            ValidationError: If election times are outside event bounds
        """
        event = (
            attrs.get('election_event') or
            self.instance.election_event if self.instance else None
        )
        start = attrs.get('start_time')
        end = attrs.get('end_time')

        # Set defaults from event if not provided
        if not start and event:
            attrs['start_time'] = event.start_time
        if not end and event:
            attrs['end_time'] = event.end_time
        
        start = attrs.get('start_time')
        end = attrs.get('end_time')

        # Validate against event timing
        if event:
            if start and start < event.start_time:
                raise ValidationError(
                    "Election start time cannot be before election event start time."
                )
            if end and end > event.end_time:
                raise ValidationError(
                    "Election end time cannot be after election event end time."
                )
            if start and end and start >= end:
                raise ValidationError(
                    "Election start time must be before end time."
                )
        
        return attrs


class CandidateSerializer(serializers.ModelSerializer):
    """
    Serializer for Candidate model instances.
    
    Handles candidate data serialization with full name generation
    and validation to prevent duplicate candidacies per election.
    
    Fields:
        id: Candidate unique identifier
        first_name: Candidate's first name
        last_name: Candidate's last name
        full_name: Computed full name (read-only)
        bio: Candidate biography
        election: Associated election ID
    """
    full_name = serializers.SerializerMethodField(
        help_text="Candidate's full name (first name + last name)"
    )

    class Meta:
        model = Candidate
        fields = [
            'id',
            'first_name',
            'last_name',
            'full_name',
            'bio',
            'election'
        ]
        extra_kwargs = {
            'first_name': {'help_text': "Candidate's first name"},
            'last_name': {'help_text': "Candidate's last name"},
            'bio': {'help_text': "Candidate's biography and platform"},
            'election': {'help_text': "ID of the election for this candidacy"}
        }
    
    def get_full_name(self, obj):
        """
        Creates and returns fullname from first name and last name fields.
        """
        return f"{obj.first_name} {obj.last_name}"
    
    def validate(self, data):
        """
        Ensures a user can be a candidate once per election.
        """
        user = data.get('user')
        election = data.get('election')

        if self.instance:
            if self.instance.user == user and self.instance.election == election:
                return data
        
        if Candidate.objects.filter(user=user, election=election).exists():
            raise serializers.ValidationError(
                "This user is already a candidate in this election."
            )
        
        return data

