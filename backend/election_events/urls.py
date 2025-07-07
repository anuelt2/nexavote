"""
election_events/urls.py

URL configuration for the election_events application.
This module defines the URL patterns for election event related views.
"""
from django.urls import path
from election_events.views import ElectionEventListView, VoterElectionEventDetailView, ElectionEventCreateView


urlpatterns = [
    path('', ElectionEventListView.as_view(), name='election-event-list'),
    path('event/', VoterElectionEventDetailView.as_view(), name='election-event-detail'),
    path('election_events/admin/add-election-event/', ElectionEventCreateView.as_view(), name='add-election-event'),
]