"""
"""
from django.views import View
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import generics, permissions

from elections.models import Election, Candidate
from elections.serializers import ElectionSerializer, CandidateSerializer
from users.models import VoterProfile
from votes.models import Vote


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



class VoterElectionListView(LoginRequiredMixin, ListView):
    """
    """
    model = Election
    template_name = "elections/election_list.html"
    context_object_name = "elections"

    def get_queryset(self):
        """
        """
        profile = get_object_or_404(VoterProfile, user=self.request.user)
        return Election.objects.filter(election_event=profile.election_event)


class VoterElectionDetailView(LoginRequiredMixin, View):
    """
    """
    def get(self, request, pk):
        """
        """
        profile = request.user.voterprofile
        election = get_object_or_404(Election, pk=pk, election_event=profile.election_event)
        candidates = Candidate.objects.filter(election=election)

        just_voted = request.session.get("just_voted", False)
        has_voted = Vote.objects.filter(voter=request.user.voterprofile, candidate__election=election).exists()

        show_form = not has_voted and not just_voted

        if just_voted:
            messages.success(request, "Your vote has been submitted successfully.")
            request.session.pop("just_voted", None)

        context = {
            "election": election,
            "candidates": candidates,
            "has_voted": has_voted and not just_voted,
            "just_voted": just_voted,
            "show_form": show_form,
        }

        return render(request, "elections/election_detail.html", context)
    
    def post(self, request, pk):
        """
        """
        profile = request.user.voterprofile
        election = get_object_or_404(Election, pk=pk, election_event=profile.election_event)

        if Vote.objects.filter(voter=request.user.voterprofile, candidate__election=election).exists():
            return redirect("election-detail", pk=pk)
        
        candidate_id = request.POST.get("candidate")
        candidate = get_object_or_404(Candidate, pk=candidate_id, election=election)

        Vote.objects.create(voter=request.user.voterprofile, candidate=candidate)

        request.session["just_voted"] = True

        return redirect("election-detail", pk=pk)