"""
"""
from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics

from election_events.models import ElectionEvent
from election_events.serializers import ElectionEventSerializer
from users.models import VoterProfile


class ElectionEventListView(generics.ListAPIView):
    """
    """
    queryset = ElectionEvent.objects.all()
    serializer_class = ElectionEventSerializer


class VoterElectionEventDetailView(LoginRequiredMixin, View):
    """
    """
    def get(self, request):
        """
        """
        profile = get_object_or_404(VoterProfile, user=request.user)
        event = profile.election_event

        return render(request, "election_events/election_event_detail.html", {
            "election_event": event
        })