"""
votes/urls.py
URL configuration for vote-related endpoints.
"""
from django.urls import path
from votes.views import (
    CastVoteView,
    VoterVotesListView,
    VoteDetailView,
    VoteAuditLogListView,
    ElectionResultsView,
    ElectionEventParticipationView,
    ElectionsAvailableView,
    check_vote_status,
    verify_vote,
    election_statistics
)

app_name = 'votes'

urlpatterns = [
    # Vote Casting & Management
    path('', CastVoteView.as_view(), name='cast-vote'),
    path('my-votes/', VoterVotesListView.as_view(), name='my-votes'),
    path('<uuid:pk>/', VoteDetailView.as_view(), name='vote-detail'),
    
    # Vote Verification
    path('verify/', verify_vote, name='verify-vote'),
    path('check-status/<uuid:election_id>/', check_vote_status, name='check-vote-status'),
    
    # Election Results and Statistics
    path('results/<uuid:election_id>/', ElectionResultsView.as_view(), name='election-results'),
    path('statistics/<uuid:election_id>/', election_statistics, name='election-statistics'),
    
    # Election Event Participation
    path('participation/<uuid:event_id>/', ElectionEventParticipationView.as_view(), name='event-participation'),
    path('elections-available/', ElectionsAvailableView.as_view(), name='elections-available'),
    
    # Audit Logs
    path('audit-logs/', VoteAuditLogListView.as_view(), name='audit-logs'),
]