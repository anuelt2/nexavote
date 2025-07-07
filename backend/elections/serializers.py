"""
"""
from django.core.exceptions import ValidationError
from rest_framework import serializers
from elections.models import Election, Candidate


class ElectionSerializer(serializers.ModelSerializer):
    """
    Serializer for Election model.
    """
    class Meta:
        model = Election
        fields = [
            'id',
            'title',
            'description',
            'start_time',
            'end_time',
            'is_active',
            'election_event'
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
    """
    class Meta:
        model = Candidate
        fields = [
            'id',
            'first_name',
            'last_name',
            'bio',
            'election',
            'user'
        ]