"""
"""
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