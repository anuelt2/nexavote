"""
"""
from rest_framework import generics, permissions

from elections.models import Election, Candidate
from elections.serializers import ElectionSerializer, CandidateSerializer


class ElectionListView(generics.ListAPIView):
    """
    List elections within a specific election event.
    """
    serializer_class = ElectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        """
        event_id = self.request.query_params.get('event')
        if event_id:
            return Election.objects.filter(election_event__id=event_id)
        return Election.objects.all()


class CandidateListView(generics.ListAPIView):
    """
    List candidates within a specific election  event.
    """
    serializer_class = CandidateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        """
        election_id = self.request.query_params.get('election')
        if election_id:
            return Candidate.objects.filter(election__id=election_id)
        return Candidate.objects.all()
    

class ElectionAdminCreateView(generics.CreateAPIView):
    """
    """
    queryset = Election.objects.all()
    serializer_class = ElectionSerializer
    permission_classes = [permissions.IsAdminUser]

class ElectionAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    """
    queryset = Election.objects.all()
    serializer_class = ElectionSerializer
    permission_calsses = [permissions.IsAdminUser]

class CandidateAdminCreateView(generics.CreateAPIView):
    """
    """
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [permissions.IsAdminUser]

class CandidateAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    """
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [permissions.IsAdminUser]
