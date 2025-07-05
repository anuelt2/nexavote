"""
"""
from django.urls import path
from election_events.views import ElectionEventListView, VoterElectionEventDetailView


urlpatterns = [
    path('', ElectionEventListView.as_view(), name='election-event-list'),
    path('event/', VoterElectionEventDetailView.as_view(), name='election-event-detail'),
]