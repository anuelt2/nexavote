"""
elections/urls.py

URL configuration for the elections application.
This module defines the URL patterns for election and candidate related views.
"""
from django.urls import path
from elections.views import (
    VoterElectionListView, VoterElectionDetailView,
    AdminElectionResultsView, CandidateCreateView,
    ElectionCreateView, AdminElectionListView
)


urlpatterns = [
    # Admin Template views
    path('elections/admin/results/', AdminElectionResultsView.as_view(), name='admin-results'),
    path('elections/admin/<uuid:election_id>/add-candidate/', CandidateCreateView.as_view(), name='add-candidate'),
    path('elections/admin/add-election/', ElectionCreateView.as_view(), name='add-election'),
    path('elections/admin/add-election/<uuid:event_id>/', ElectionCreateView.as_view(), name='add-election-for-election-event'),
    path('elections/admin/dashboard/', AdminElectionListView.as_view(), name='admin-dashboard'),

    # Voter Template views
    path('my-elections/', VoterElectionListView.as_view(), name='election-list'),
    path('vote/<uuid:pk>/', VoterElectionDetailView.as_view(), name='vote-page'),
]