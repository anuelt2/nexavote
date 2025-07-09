"""
election_events/serializers.py

This module defines Django REST Framework serializers for the election_events app.
"""
from rest_framework import serializers
from election_events.models import ElectionEvent


class ElectionEventSerializer(serializers.ModelSerializer):
    """
    Serializer for ElectionEvent model.
    
    This serializer handles the conversion between ElectionEvent model instances
    and JSON representation for API responses and requests.
    
    Meta:
        model: The ElectionEvent model class
        fields: List of fields to include in serialization
    """
    class Meta:
        model = ElectionEvent
        fields = [
            'id',
            'title',
            'description',
            'start_time',
            'end_time',
            'is_active'         
        ]
    
    def validate(self, data):
        """
        Validation for election_event start and end times.
        """
        if data['end_time'] <= data['start_time']:
            raise serializers.ValidationError("End time must be after start time.")
        return data