"""
election_events/urls.py

URL configuration for the election_events application.
This module defines the URL patterns for election event related views.
"""
from django.urls import path
from election_events.views import VoterElectionEventDetailView, ElectionEventCreateView


urlpatterns = [
    # Template views (voter-facing)
    path('my-event/', VoterElectionEventDetailView.as_view(), name='voter-event-detail'),

    # Template views (Admin)
    path('admin/add/', ElectionEventCreateView.as_view(), name='add-election-event'),
]