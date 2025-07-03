"""
votes/views.py
Views for handling vote-related operations including casting votes,
viewing results, and managing vote audit logs.
"""
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from django.core.exceptions import ValidationError

from .models import Vote, VoteAuditLog
from .serializers import (
    VoteCastSerializer, VoteDetailSerializer, VoteResultSerializer,
    ElectionResultsSerializer, VoterParticipationSerializer,
    VoteAuditLogSerializer, VoteVerificationSerializer
)
from elections.models import Election, ElectionEvent
from users.models import VoterProfile
from users.permissions import IsVoter, IsElectionAdmin


class CastVoteView(generics.CreateAPIView):
    """
    API view for casting a vote.
    Only authenticated voters can cast votes.
    """
    serializer_class = VoteCastSerializer
    permission_classes = [permissions.IsAuthenticated, IsVoter]
    
    def perform_create(self, serializer):
        """
        Create vote and log the action.
        """
        vote = serializer.save()
        
        # Create audit log
        VoteAuditLog.objects.create(
            vote=vote,
            action='cast',
            performed_by=self.request.user,
            details=f"Vote cast for candidate {vote.candidate.first_name} {vote.candidate.last_name}",
            ip_address=self.get_client_ip()
        )
    
    def get_client_ip(self):
        """
        Get client IP address from request.
        """
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip


class VoterVotesListView(generics.ListAPIView):
    """
    API view for listing votes cast by the authenticated voter.
    """
    serializer_class = VoteDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsVoter]
    
    def get_queryset(self):
        """
        Return votes for the authenticated user.
        """
        try:
            voter = VoterProfile.objects.get(user=self.request.user)
            return Vote.objects.filter(voter=voter).select_related(
                'candidate', 'candidate__election', 'voter__user'
            )
        except VoterProfile.DoesNotExist:
            return Vote.objects.none()


class ElectionResultsView(generics.RetrieveAPIView):
    """
    API view for getting election results.
    Only accessible after election ends or by election admins.
    """
    serializer_class = ElectionResultsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """
        Get election and verify access permissions.
        """
        election_id = self.kwargs['election_id']
        election = get_object_or_404(Election, id=election_id)
        
        # Check if user can view results
        if not (election.has_ended() or 
                self.request.user.groups.filter(name='ElectionAdmins').exists()):
            self.permission_denied(
                self.request,
                message="Results not available yet."
            )
        
        return election
    
    def retrieve(self, request, *args, **kwargs):
        """
        Return election results.
        """
        election = self.get_object()
        results = Vote.get_election_results(election)
        
        # Format results for serializer
        formatted_results = [
            {'candidate_name': name, 'vote_count': count}
            for name, count in results.items()
        ]
        
        data = {
            'election_id': election.id,
            'election_title': election.title,
            'total_votes': sum(results.values()),
            'results': formatted_results
        }
        
        serializer = self.get_serializer(data)
        return Response(serializer.data)


class ElectionEventParticipationView(generics.RetrieveAPIView):
    """
    API view for getting voter participation statistics for an election event.
    """
    serializer_class = VoterParticipationSerializer
    permission_classes = [permissions.IsAuthenticated, IsElectionAdmin]
    
    def get_object(self):
        """
        Get election event.
        """
        event_id = self.kwargs['event_id']
        return get_object_or_404(ElectionEvent, id=event_id)
    
    def retrieve(self, request, *args, **kwargs):
        """
        Return participation statistics.
        """
        election_event = self.get_object()
        stats = Vote.get_voter_participation(election_event)
        
        serializer = self.get_serializer(stats)
        return Response(serializer.data)


class VoteAuditLogListView(generics.ListAPIView):
    """
    API view for listing vote audit logs.
    Only accessible by election admins.
    """
    serializer_class = VoteAuditLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsElectionAdmin]
    filterset_fields = ['action', 'vote__candidate__election']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Return audit logs with related data.
        """
        return VoteAuditLog.objects.select_related(
            'vote', 'vote__voter__user', 'vote__candidate', 
            'vote__candidate__election', 'performed_by'
        )


class VoteDetailView(generics.RetrieveAPIView):
    """
    API view for getting vote details.
    Voters can only see their own votes, admins can see all votes.
    """
    serializer_class = VoteDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Return appropriate queryset based on user permissions.
        """
        if self.request.user.groups.filter(name='ElectionAdmins').exists():
            return Vote.objects.all()
        else:
            try:
                voter = VoterProfile.objects.get(user=self.request.user)
                return Vote.objects.filter(voter=voter)
            except VoterProfile.DoesNotExist:
                return Vote.objects.none()


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def verify_vote(request):
    """
    API endpoint for verifying a vote using its hash.
    """
    serializer = VoteVerificationSerializer(data=request.data)
    if serializer.is_valid():
        vote_hash = serializer.validated_data['vote_hash']
        try:
            vote = Vote.objects.get(vote_hash=vote_hash)
            return Response({
                'verified': True,
                'vote_id': vote.id,
                'election_title': vote.candidate.election.title,
                'candidate_name': f"{vote.candidate.first_name} {vote.candidate.last_name}",
                'created_at': vote.created_at,
                'is_verified': vote.is_verified
            })
        except Vote.DoesNotExist:
            return Response({
                'verified': False,
                'message': 'Vote hash not found'
            }, status=status.HTTP_404_NOT_FOUND)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def check_vote_status(request, election_id):
    """
    Check if the authenticated user has voted in a specific election.
    """
    try:
        voter = VoterProfile.objects.get(user=request.user)
        election = get_object_or_404(Election, id=election_id)
        
        vote_exists = Vote.objects.filter(
            voter=voter,
            candidate__election=election
        ).exists()
        
        return Response({
            'has_voted': vote_exists,
            'election_id': election.id,
            'election_title': election.title,
            'election_status': election.get_status_display() if hasattr(election, 'get_status_display') else 'active'
        })
        
    except VoterProfile.DoesNotExist:
        return Response({
            'error': 'Voter profile not found'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsElectionAdmin])
def election_statistics(request, election_id):
    """
    Get detailed statistics for a specific election.
    """
    election = get_object_or_404(Election, id=election_id)
    
    # Basic vote counts
    total_votes = Vote.objects.filter(
        candidate__election=election,
        is_verified=True
    ).count()
    
    # Votes by candidate
    candidate_votes = Vote.objects.filter(
        candidate__election=election,
        is_verified=True
    ).values(
        'candidate__first_name',
        'candidate__last_name'
    ).annotate(
        vote_count=Count('id')
    ).order_by('-vote_count')
    
    # Voting timeline (votes per hour/day)
    from django.db.models.functions import TruncHour
    voting_timeline = Vote.objects.filter(
        candidate__election=election,
        is_verified=True
    ).annotate(
        hour=TruncHour('created_at')
    ).values('hour').annotate(
        vote_count=Count('id')
    ).order_by('hour')
    
    return Response({
        'election_id': election.id,
        'election_title': election.title,
        'total_votes': total_votes,
        'candidate_results': list(candidate_votes),
        'voting_timeline': list(voting_timeline),
        'verification_stats': {
            'verified_votes': Vote.objects.filter(
                candidate__election=election, 
                is_verified=True
            ).count(),
            'unverified_votes': Vote.objects.filter(
                candidate__election=election, 
                is_verified=False
            ).count()
        }
    })