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
    
    Attributes:
        title (CharField): The name/title of the election event
        description (TextField): Detailed description of the election event
        start_time (DateTimeField): When the election event begins
        end_time (DateTimeField): When the election event ends
        is_active (BooleanField): Whether the election event is currently active
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def is_open(self):
        """
        Check if the election event is currently open for voting.
        
        An election event is considered open if it's active and the current
        time falls within the start and end time window.
        
        Returns:
            bool: True if the election event is open, False otherwise
        """
        now = timezone.now()
        return self.is_active and self.start_time <= now <= self.end_time

    def __str__(self):
        """
        Return string representation of the election event.
        
        Returns:
            str: The title of the election event
        """
        return self.title