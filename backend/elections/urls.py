"""
"""
from django.urls import path
from elections.views import (
    ElectionListView, CandidateListView,
    ElectionAdminCreateView, ElectionAdminDetailView,
    CandidateAdminCreateView, CandidateAdminDetailView
)


urlpatterns = [
    # Voter views
    path('elections/', ElectionListView.as_view(), name='election-list'),
    path('candidates/', CandidateListView.as_view(), name='candidate-list'),

    # Admin views
    path('elections/admin/', ElectionAdminCreateView.as_view(), name='election-admin-create'),
    path('elections/admin/<uuid:pk>/', ElectionAdminDetailView.as_view(), name='election-admin-detail'),

    path('candidates/admin', CandidateAdminCreateView.as_view(), name='candidate-admin-create'),
    path('candidates/admin/<uuid:pk>/', CandidateAdminDetailView.as_view(), name='candidate-admin-detail'),
]