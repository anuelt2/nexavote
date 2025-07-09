"""
elections/urls_api.py

URL configuration for the elections application.
This module defines the URL patterns for election and candidate related views.
"""
from django.urls import path
from elections.views import (
    ElectionListView,
    ElectionCreateAPIView,
    ElectionRetrieveAPIView,
    ElectionUpdateAPIView,
    ElectionDeleteAPIView,
    CandidateListView,
    CandidateAdminCreateView,
    CandidateRetrieveAPIView,
    CandidateUpdateAPIView,
    CandidateDeleteAPIView
)


urlpatterns = [
    # Admin Access API routes
    path('elections/admin/create/', ElectionCreateAPIView.as_view(), name='election-create'),
    path('elections/admin/<uuid:pk>/update/', ElectionUpdateAPIView.as_view(), name='election-update'),
    path('elections/admin/<uuid:pk>/delete', ElectionDeleteAPIView.as_view(), name='election-delete'),
    path('candidates/admin/create/', CandidateAdminCreateView.as_view(), name='candidate-create'),
    path('candidates/admin/<uuid:pk>/', CandidateRetrieveAPIView.as_view(), name='candidate-detail'),
    path('candidates/admin/<uuid:pk>/update/', CandidateUpdateAPIView.as_view(), name='candidate-update'),
    path('candidates/admin/<uuid:pk>/delete/', CandidateDeleteAPIView.as_view(), name='candidate-delete'),
    
    # Admin + Voter Access API routes
    path('elections/<uuid:pk>/', ElectionRetrieveAPIView.as_view(), name='election-detail'),
    path('elections/list/', ElectionListView.as_view(), name='election-list'),
    path('candidates/<uuid:election_id>/election', CandidateListView.as_view(), name='candidates-by-election'),
]