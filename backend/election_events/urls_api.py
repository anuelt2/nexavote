"""
election_events/urls_api.py

URL configuration for the election_events application.
This module defines the URL patterns for election event related api views.
"""
from django.urls import path
from election_events.views import (
    ElectionEventListView,
    ElectionEventDetailView,
    ElectionEventVoterView,
    ElectionEventCreateAPIView,
    ElectionEventUpdateView,
    ElectionEventDeleteView
)

urlpatterns = [
    path('', ElectionEventListView.as_view(), name='event-list'),
    path('<uuid:pk>/', ElectionEventDetailView.as_view(), name='event-detail'),
    path('my-event/', ElectionEventVoterView.as_view(), name='my-event'),
    path('create/', ElectionEventCreateAPIView.as_view(), name='event-create'),
    path('<uuid:pk>/update/', ElectionEventUpdateView.as_view(), name='event-update'),
    path('<uuid:pk>/delete/', ElectionEventDeleteView.as_view(), name='event-delete'),
]