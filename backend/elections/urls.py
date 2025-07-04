"""
"""
from django.urls import path
from elections.views import (
    ElectionListView, CandidateListView,
    ElectionAdminCreateView, ElectionAdminDetailView,
    CandidateAdminCreateView, CandidateAdminDetailView,
    VoterElectionListView, VoterElectionDetailView
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
    path('elections/<uuid:pk>/', VoterElectionDetailView.as_view(), name='election-detail')
]