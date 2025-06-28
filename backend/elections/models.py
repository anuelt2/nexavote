"""
elections/models.py

This module defines the Election model for creating
and managing elections and also the Candidate model.

Each election has candidates to choose from and a time window
for voting.
"""
from django.db import models
from django.utils import timezone
from django.conf import settings

from core.models import BaseUUIDModel
from election_events.models import ElectionEvent


class Election(BaseUUIDModel):
    """
    Election model representing a specific voting event within an
    election event.
    """
    election_event = models.ForeignKey(
        ElectionEvent,
        on_delete=models.CASCADE,
        related_name='elections'
    )
    title = models.CharField(max_length=225)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def is_open(self):
        """
        """
        now = timezone.now()
        return self.is_active and self.start_time <= now <= self.end_time
    
    def _str__(self):
        """
        Return string representation with election title and
        election_event title.
        """
        return f"{self.title} ({self.election_event.title})"


class Candidate(BaseUUIDModel):
    """
    Candidate model representing a candidate contesting in a specific
    election within a specific election event.

    Candidate may optionally be a registered voter.
    """
    election = models.ForeignKey(
        Election,
        on_delete=models.CASCADE,
        related_name='candidates'
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    bio = models.TextField(blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='candidates'
    )

    def __str__(self):
        """
        Return string representation with candidate name and
        election contested.
        """
        return f"{self.name} ({self.election.title})"