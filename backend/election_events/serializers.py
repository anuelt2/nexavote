"""
"""
from rest_framework import serializers

from election_events.models import ElectionEvent


class ElectionEventSerializer(serializers.ModelSerializer):
    """
    Serializer for ElectionEvent model.
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