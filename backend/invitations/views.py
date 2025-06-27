"""
"""
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

from invitations.models import Invitation
from invitations.serializers import InvitationCreateSerializer
# from elections.models import Election


class InvitationCreateAPIView(generics.CreateAPIView):
    """
    """
    queryset = Invitation.objects.all()
    serializer_class = InvitationCreateSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        """
        """
        invitation = serializer.save()
        self.send_invite_email(invitation)

    def send_invite_email(self, invitation):
        """
        """
        registration_url = f"http://localhost:8000/register?token={invitation.token}"
        subject = "You are invited to register for NexaVote Election"     # replace NexaVote with election title
        message = (
            f"Hello,\n\n"
            f"You have been invited to register as a voter in NexaVote Election."   # replace NexaVote with election title
            f"Please click on the link below to complete your registration:\n\n"
            f"{registration_url}\n\n"
            f"If you did not expect this invitation, please ignore this email.\n\n"
            f"Thanks."
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [invitation.email],
            fail_silently=False,
        )