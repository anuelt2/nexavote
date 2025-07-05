"""
"""
from django.urls import path
from invitations.views import InvitationCreateAPIView, InvitationCreateView


urlpatterns =[
    path('create/', InvitationCreateAPIView.as_view(), name='invitation-create'),
    path('invite/', InvitationCreateView.as_view(), name='invite-voter'),
]