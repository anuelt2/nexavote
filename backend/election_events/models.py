"""
election_events/models.py

This module defines the ElectionEvent model for creating and managing
election events.
"""
from django.db import models
from django.utils import timezone

from core.models import BaseUUIDModel


class ElectionEvent(BaseUUIDModel):
    """
    ElectionEvent model representing one election period, consisting
    at least one election.

    Election events consist of at least one election of a group of
    candidates.
    
    It also defines the voter eligibility for that election event.
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def is_open(self):
        """
        """
        now = timezone.now()
        return self.is_active and self.start_time <= now <= self.end_time

    def __str__(self):
        """
        Return string representation with election event title.
        """
        return self.title