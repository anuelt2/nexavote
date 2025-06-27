"""
"""
from django.urls import path
from invitations.views import InvitationCreateAPIView


urlpatterns =[
    path(
        'create/',
        InvitationCreateAPIView.as_view(),
        name='invitation-create'
    ),
]