"""
invitations/models.py

This module defines the Invitation model for managing tokens used to register
voters.

Each invitation consists of a unique email and a UUID token, for one-time use,
to control voter registration access.
"""
import uuid
from django.db import models

from core.models import BaseUUIDModel


class Invitation(BaseUUIDModel):
    """
    Invitation model representing an invite to register as a voter.
    """
    email = models.EmailField(unique=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        """
        Return string representation with user email and invitation use status.
        """
        return f'{self.email} - Used: {self.is_used}'
