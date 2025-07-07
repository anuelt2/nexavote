"""
invitations/models.py

This module defines the Invitation model for managing tokens used to register
voters.

Each invitation consists of a unique email and a UUID token, for one-time use,
to control voter registration access.
"""
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from core.models import BaseUUIDModel
from election_events.models import ElectionEvent

User = get_user_model()


class Invitation(BaseUUIDModel):
    """
    Invitation model representing an invite to register as a voter.
    """
    email = models.EmailField(unique=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_used = models.BooleanField(default=False)
    election_event = models.ForeignKey(
        ElectionEvent,
        on_delete=models.CASCADE,
        related_name='invitations'
    )
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    invited_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='sent_invitations'
    )

    def __str__(self):
        """
        Return string representation with user email and invitation use status.
        """
        return f'{self.email} - Used: {self.is_used}'
