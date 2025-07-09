"""
elections/views.py

This module defines views for the elections application.
Contains both API views and HTML template views for election and candidate management.
"""
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Prefetch
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView

from rest_framework import generics, permissions

from elections.forms import CandidateForm, ElectionForm
from elections.models import Election, Candidate
from election_events.models import ElectionEvent
from elections.serializers import ElectionSerializer, CandidateSerializer
from users.models import VoterProfile
from users.permissions import IsElectionAdmin
from votes.models import Vote


# === API Views ===

class ElectionCreateAPIView(generics.CreateAPIView):
    """
    API view for creating new elections (admin only).
    
    This view allows administrators to create new elections via POST requests.
    
    Attributes:
        queryset: All Election objects
        serializer_class: ElectionSerializer for JSON serialization
        permission_classes: Requires admin privileges
    """
    queryset = Election.objects.all()
    serializer_class = ElectionSerializer
    permission_classes = [permissions.IsAuthenticated, IsElectionAdmin]


class ElectionListView(generics.ListAPIView):
    """
    API view for listing all elections for Admin only and a voter's elections.
    
    This view provides a read-only endpoint that returns a list of elections.
    
    Attributes:
        serializer_class: ElectionSerializer for JSON serialization
        permission_classes: Requires authentication
    """
    queryset = Election.objects.select_related('election_event')
    serializer_class = ElectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Get the queryset of elections.
        
        Returns:
            QuerySet: All elections for admin or voter's elections.
        """
        user = self.request.user
        if user.is_staff:
            return self.queryset.all()
        try:
            voter = VoterProfile.objects.get(user=user)
            return self.queryset.filter(election_event=voter.election_event)
        except VoterProfile.DoesNotExist:
            return Election.objects.none()


class ElectionRetrieveAPIView(generics.RetrieveAPIView):
    """
    API view for retrieving details of a specific election.
    - Admins can retrieve any election.
    - Voters can retrieve any election from their election event.
    """
    queryset = Election.objects.select_related('election_event')
    serializer_class = ElectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    llokup_field = 'pk'

    def get_queryset(self):
        """
        Get the queryset of elections.
        
        Returns:
            QuerySet: A particular election.
        """
        user = self.request.user
        if user.is_staff:
            return self.queryset.all()
        try:
            voter = VoterProfile.objects.get(user=user)
            return self.queryset.filter(election_event=voter.election_event)
        except VoterProfile.DoesNotExist:
            return Election.objects.none()


class ElectionUpdateAPIView(generics.UpdateAPIView):
    """
    API view for updating elections (admin only).
    
    This view allows administrators to perform CRUD operations on individual elections.
    
    Attributes:
        queryset: All Election objects
        serializer_class: ElectionSerializer for JSON serialization
        permission_classes: Requires admin privileges
    """
    queryset = Election.objects.all()
    serializer_class = ElectionSerializer
    permission_classes = [permissions.IsAuthenticated, IsElectionAdmin]
    lookup_field = 'pk'


class ElectionDeleteAPIView(generics.DestroyAPIView):
    """
    API view for deleting elections (admin only).
    
    This view allows administrators to perform CRUD operations on individual elections.
    
    Attributes:
        queryset: All Election objects
        serializer_class: ElectionSerializer for JSON serialization
        permission_classes: Requires admin privileges
    """
    queryset = Election.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsElectionAdmin]
    lookup_field = 'pk'


class CandidateAdminCreateView(generics.CreateAPIView):
    """
    API view for creating new candidates for a specific election (admin only).
    
    This view allows administrators to create new candidates via POST requests.
    
    Attributes:
        queryset: Related Candidate objects
        serializer_class: CandidateSerializer for JSON serialization
        permission_classes: Requires admin privileges
    """
    queryset = Candidate.objects.select_related('election', 'user')
    serializer_class = CandidateSerializer
    permission_classes = [permissions.IsAuthenticated, IsElectionAdmin]


class CandidateRetrieveAPIView(generics.RetrieveAPIView):
    """
    API view for retrieving candidates (admin only).
    
    This view allows administrators to perform CRUD operations on individual candidates.
    
    Attributes:
        queryset: Related Candidate objects
        serializer_class: CandidateSerializer for JSON serialization
        permission_classes: Requires admin privileges
    """
    queryset = Candidate.objects.select_related('election', 'user')
    serializer_class = CandidateSerializer
    permission_classes = [permissions.IsAuthenticated, IsElectionAdmin]
    lookup = 'pk'


class CandidateUpdateAPIView(generics.UpdateAPIView):
    """
    API view for updating candidates (admin only).
    
    This view allows administrators to perform CRUD operations on individual candidates.
    
    Attributes:
        queryset: Related Candidate objects
        serializer_class: CandidateSerializer for JSON serialization
        permission_classes: Requires admin privileges
    """
    queryset = Candidate.objects.select_related('election', 'user')
    serializer_class = CandidateSerializer
    permission_classes = [permissions.IsAuthenticated, IsElectionAdmin]
    lookup = 'pk'


class CandidateDeleteAPIView(generics.DestroyAPIView):
    """
    API view for deleting candidates (admin only).
    
    This view allows administrators to perform CRUD operations on individual candidates.
    
    Attributes:
        queryset: Related Candidate objects
        serializer_class: CandidateSerializer for JSON serialization
        permission_classes: Requires admin privileges
    """
    queryset = Candidate.objects.select_related('election', 'user')
    permission_classes = [permissions.IsAuthenticated, IsElectionAdmin]
    lookup = 'pk'


class CandidateListView(generics.ListAPIView):
    """
    API view for listing candidates within a specific election.
    
    This view provides a read-only endpoint that returns a list of candidates.
    It can be filtered by election ID via query parameters.
    
    Attributes:
        serializer_class: CandidateSerializer for JSON serialization
        permission_classes: Requires authentication
    """
    serializer_class = CandidateSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'election_id'

    def get_queryset(self):
        """
        Get the queryset of candidates, optionally filtered by election.
        
        Returns:
            QuerySet: Candidates filtered by election ID if provided, otherwise all candidates
        """
        election_id = self.kwargs['election_id']
        if election_id:
            return Candidate.objects.filter(election__id=election_id)
        return Candidate.objects.none()


# === Template Views ===

class VoterElectionListView(LoginRequiredMixin, ListView):
    """
    HTML view for displaying elections to authenticated voters.
    
    This view shows a list of elections that belong to the voter's election event.
    
    Attributes:
        model: The Election model
        template_name: Template for rendering the election list
        context_object_name: Context variable name for the elections
    """
    model = Election
    template_name = "elections/election_list.html"
    context_object_name = "elections"

    def get_queryset(self):
        """
        Get elections for the authenticated voter's election event.
        
        Returns:
            QuerySet: Elections belonging to the voter's election event
        """
        profile = get_object_or_404(VoterProfile, user=self.request.user)
        return Election.objects.filter(election_event=profile.election_event)


class VoterElectionDetailView(LoginRequiredMixin, View):
    """
    HTML view for displaying election details and handling voting.
    
    This view shows election details, candidates, and handles the voting process
    for authenticated voters.
    """
    def get(self, request, pk):
        """
        Handle GET requests to display election details and voting form.
        
        Args:
            request: The HTTP request object
            pk: The primary key of the election
            
        Returns:
            HttpResponse: Rendered HTML template with election and voting context
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
        Handle POST requests to submit votes.
        
        Args:
            request: The HTTP request object containing vote data
            pk: The primary key of the election
            
        Returns:
            HttpResponse: Redirect to election detail page
        """
        profile = request.user.voterprofile
        election = get_object_or_404(Election, pk=pk, election_event=profile.election_event)

        # Check if user has already voted
        if Vote.objects.filter(voter=request.user.voterprofile, candidate__election=election).exists():
            return redirect("election-detail", pk=pk)
        
        # Process the vote
        candidate_id = request.POST.get("candidate")
        candidate = get_object_or_404(Candidate, pk=candidate_id, election=election)

        Vote.objects.create(voter=request.user.voterprofile, candidate=candidate)

        request.session["just_voted"] = True

        return redirect("election-detail", pk=pk)


class AdminElectionResultsView(View):
    """
    HTML view for displaying election results to administrators.
    
    This view shows vote counts for all candidates across all elections.
    Requires staff privileges.
    """
    @method_decorator(staff_member_required)
    def get(self, request):
        """
        Handle GET requests to display election results.
        
        Args:
            request: The HTTP request object
            
        Returns:
            HttpResponse: Rendered HTML template with election results
        """
        elections = Election.objects.all().prefetch_related('candidates__votes', 'candidates')
        results = []

        for election in elections:
            candidates = election.candidates.all()
            candidate_data = []
            for candidate in candidates:
                vote_count = candidate.votes.count()
                candidate_data.append({
                    "name": f"{candidate.first_name} {candidate.last_name}",
                    "votes": vote_count,
                })
            results.append({
                "election": election,
                "candidates": candidate_data
            })
        
        return render(request, "elections/admin_results.html", {"results": results})


class ElectionCreateView(View):
    """
    HTML view for creating new candidates (admin only).
    
    This view provides a form interface for administrators to create new candidates.
    Requires staff privileges.
    """
    @method_decorator(staff_member_required)
    def get(self, request, event_id=None):
        """
        Handle GET requests to display candidate creation form.
        
        Args:
            request: The HTTP request object
            
        Returns:
            HttpResponse: Rendered HTML template with candidate creation form
        """
        event = None
        initial = {}

        if event_id:
            event = get_object_or_404(ElectionEvent, id=event_id, is_active=True)
            initial['election_event'] = event

        form = ElectionForm()
        return render(request, "elections/election_create.html", {"form": form, "event": event})
    
    @method_decorator(staff_member_required)
    def post(self, request):
        """
        Handle POST requests to create new candidates.
        
        Args:
            request: The HTTP request object containing form data
            
        Returns:
            HttpResponse: Redirect to election results or form with errors
        """
        form = ElectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("election-results")
        return render(request, "elections/election_create.html", {"form": form})


class AdminElectionListView(View):
    """
    HTML view for creating new elections (admin only).
    
    This view provides a form interface for administrators to create new elections.
    Requires staff privileges.
    """
    @method_decorator(staff_member_required)
    def get(self, request):
        """
        Handle GET requests to display election creation form.
        
        Args:
            request: The HTTP request object
            
        Returns:
            HttpResponse: Rendered HTML template with election creation form
        """
        event_qs = (
            ElectionEvent.objects
            .filter(elections__isnull=False)
            .annotate(election_count=Count('elections'))
            .prefetch_related(
                Prefetch(
                    'elections',
                    queryset=(
                        Election.objects
                        .prefetch_related('candidates')
                        .annotate(vote_count=Count('candidates__votes'))
                        .order_by('start_time')
                    )
                )
            )
            .order_by('title')
        )

        return render(request, "elections/admin_elections_list.html", {"events": event_qs})


class CandidateCreateView(View):
    """
    Create a candidate for a particular election
    """
    @method_decorator(staff_member_required)
    def get(self, request, election_id):
        """
        """
        election = get_object_or_404(Election, id=election_id)
        form = CandidateForm()
        return render(request, "elections/candidate_create.html", {"form": form, "election": election})
    
    @method_decorator(staff_member_required)
    def post(self, request, election_id):
        """
        Handle POST requests to create new elections.
        
        Args:
            request: The HTTP request object containing form data
            
        Returns:
            HttpResponse: Redirect to election results or form with errors
        """
        election = get_object_or_404(Election, id=election_id)
        form = CandidateForm(request.POST)
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.election = election
            candidate.save()
            return redirect("admin-elections")
        return render(request, "elections/candidate_create.html", {"form": form, "election": election})
