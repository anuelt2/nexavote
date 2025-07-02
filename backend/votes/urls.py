"""
votes/urls.py
URL configuration for vote-related endpoints.
"""
from django.urls import path
from . import views

app_name = 'votes'

urlpatterns = [
    # Vote casting
    path('', views.CastVoteView.as_view(), name='cast-vote'),
    
    # Vote management
    path('my-votes/', views.VoterVotesListView.as_view(), name='my-votes'),
    path('<uuid:pk>/', views.VoteDetailView.as_view(), name='vote-detail'),
    
    # Vote verification
    path('verify/', views.verify_vote, name='verify-vote'),
    path('check-status/<uuid:election_id>/', views.check_vote_status, name='check-vote-status'),
    
    # Election results and statistics
    path('results/<uuid:election_id>/', views.ElectionResultsView.as_view(), name='election-results'),
    path('statistics/<uuid:election_id>/', views.election_statistics, name='election-statistics'),
    
    # Election event participation
    path('participation/<uuid:event_id>/', views.ElectionEventParticipationView.as_view(), name='event-participation'),
    
    # Audit logs
    path('audit-logs/', views.VoteAuditLogListView.as_view(), name='audit-logs'),
]