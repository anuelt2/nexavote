"""
"""
from django.urls import path
from elections.views import (
    ElectionListView, CandidateListView,
    ElectionAdminCreateView, ElectionAdminDetailView,
    CandidateAdminCreateView, CandidateAdminDetailView,
    VoterElectionListView, VoterElectionDetailView,
    AdminElectionResultsView, CandidateCreateView,
    ElectionCreateView, AdminElectionListView
)


urlpatterns = [
    # Voter API routes
    path('elections/voter/', ElectionListView.as_view(), name='election-list'),
    path('candidates/', CandidateListView.as_view(), name='candidate-list'),

    # Admin API routes
    path('elections/admin/', ElectionAdminCreateView.as_view(), name='election-admin-create'),
    path('elections/admin/<uuid:pk>/', ElectionAdminDetailView.as_view(), name='election-admin-detail'),

    path('candidates/admin', CandidateAdminCreateView.as_view(), name='candidate-admin-create'),
    path('candidates/admin/<uuid:pk>/', CandidateAdminDetailView.as_view(), name='candidate-admin-detail'),

    # HTML templates routes
    path('elections/', VoterElectionListView.as_view(), name='election-list'),
    path('elections/<uuid:pk>/', VoterElectionDetailView.as_view(), name='election-detail'),
    path('elections/admin/results/', AdminElectionResultsView.as_view(), name='election-results'),
    path('elections/admin/<uuid:election_id>/add-candidate/', CandidateCreateView.as_view(), name='add-candidate'),
    path('elections/admin/add-election/', ElectionCreateView.as_view(), name='add-election'),
    path('elections/admin/add-election/<uuid:event_id>/', ElectionCreateView.as_view(), name='add-election-for-election-event'),
    path('elections/admin/elections/', AdminElectionListView.as_view(), name='admin-elections'),
]