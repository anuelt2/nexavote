"""
"""
from django.urls import path
from elections.views import ElectionListView, CandidateListView


urlpatterns = [
    path(
        'elections/',
        ElectionListView.as_view(),
        name='election-list'
    ),
    path(
        'candidates/',
        CandidateListView.as_view(),
        name='candidate-list'
    ),
]