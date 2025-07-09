"""
Django URL configuration for invitation management.

This module defines URL patterns for invitation-related views creation
via API.
"""
from django.urls import path
from invitations.views import (
    InvitationCreateAPIView,
    InvitationListCreateView,
    InvitationDetailView,
    InvitationsByEventView,
    InvitationMarkUsedView,
    InvitationByTokenView
)

urlpatterns =[
    # API view (to be mounted under /api/invitations/)
    path('create/', InvitationCreateAPIView.as_view(), name='invitation-create'),
    path('list/', InvitationListCreateView.as_view(), name='invitation-list'),
    path('<uuid:pk>/', InvitationDetailView.as_view(), name='invitation-detail'),
    path('event/<uuid:event_id>/', InvitationsByEventView.as_view(), name='invitation-by-event'),
    path('<uuid:pk>/mark-used/', InvitationMarkUsedView.as_view(), name='invitation-mark-used'),
    path('detail-by-token/<uuid:token>/', InvitationByTokenView.as_view(), name='invitation-by-token'),
]