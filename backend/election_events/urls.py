"""
"""
from django.urls import path
from election_events.views import ElectionEventListView


urlpatterns = [
    path(
        '',
        ElectionEventListView.as_view(),
        name='election-event-list'
    ),
]