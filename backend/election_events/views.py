"""
"""
from django.views.generic import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

from rest_framework import generics

from election_events.forms import ElectionEventForm
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


class ElectionEventCreateView(View):
    """
    View to handle creation of election events by admin users
    """
    @method_decorator(staff_member_required)
    def get(self, request):
        """
        """
        form = ElectionEventForm()
        return render(request, "election_events/election_event_create.html", {"form": form})
    
    @method_decorator(staff_member_required)
    def post(self, request):
        """
        """
        form = ElectionEventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("election-results")
        return render(request, "election_events/election_event_create.html", {"form": form})