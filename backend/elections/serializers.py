"""
elections/serializers.py

This module defines Django REST Framework serializers for the elections app.
"""
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from elections.models import Election, Candidate


class ElectionSerializer(serializers.ModelSerializer):
    """
    Serializer for Election model.
    
    This serializer handles the conversion between Election model instances
    and JSON representation for API responses and requests.
    
    Meta:
        model: The Election model class
        fields: List of fields to include in serialization
    """
    election_event_title = serializers.CharField(source='election_event.title', read_only=True)

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
    
    def validate(self, attrs):
        event = (
            attrs.get('election_event') or
            self.instance.election_event if self.instance else None
        )
        start = attrs.get('start_time')
        end = attrs.get('end_time')

        if not start and event:
            attrs['start_time'] = event.start_time
        if not end and event:
            attrs['end_time'] = event.end_time
        
        start = attrs.get('start_time')
        end = attrs.get('end_time')

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
                raise serializers.ValidationError(
                    "Election start time must be before end time."
                )
        
        return attrs


class CandidateSerializer(serializers.ModelSerializer):
    """
    Serializer for Candidate model.
    
    This serializer handles the conversion between Candidate model instances
    and JSON representation for API responses and requests.

    Adds full_name field, validates that a user can only be a candidate
    once per election.
    
    Meta:
        model: The Candidate model class
        fields: List of fields to include in serialization
    """
    full_name = serializers.SerializerMethodField()

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

