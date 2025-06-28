"""
"""
from rest_framework import generics

from election_events.models import ElectionEvent
from election_events.serializers import ElectionEventSerializer


class ElectionEventListView(generics.ListAPIView):
    """
    """
    queryset = ElectionEvent.objects.all()
    serializer_class = ElectionEventSerializer
