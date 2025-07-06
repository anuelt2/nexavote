"""
elections/serializers.py

This module defines Django REST Framework serializers for the elections app.
"""
from rest_framework import serializers
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


class CandidateSerializer(serializers.ModelSerializer):
    """
    Serializer for Candidate model.
    
    This serializer handles the conversion between Candidate model instances
    and JSON representation for API responses and requests.
    
    Meta:
        model: The Candidate model class
        fields: List of fields to include in serialization
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

