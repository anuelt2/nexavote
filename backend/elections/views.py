"""
"""
from rest_framework import generics

from elections.models import Election, Candidate
from elections.serializers import ElectionSerializer, CandidateSerializer


class ElectionListView(generics.ListAPIView):
    """
    """
    serializer_class = ElectionSerializer

    def get_queryset(self):
        """
        """
        event_id = self.request.query_params.get('event')
        if event_id:
            return Election.objects.filter(election_event__id=event_id)
        return Election.objects.none()


class CandidateListView(generics.ListAPIView):
    """
    """
    serializer_class = CandidateSerializer

    def get_queryset(self):
        """
        """
        election_id = self.request.query_params.get('election')
        if election_id:
            return Candidate.objects.filter(election__id=election_id)
        return Candidate.objects.none()
