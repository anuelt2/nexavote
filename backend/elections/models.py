"""
elections/models.py

This module defines the Election model for creating
and managing elections and also the Candidate model.

Each election has candidates to choose from and a time window
for voting.
"""
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from core.models import BaseUUIDModel
from election_events.models import ElectionEvent


class Election(BaseUUIDModel):
    """
    Election model representing a specific voting event within an
    election event.
    
    An election is a specific contest (e.g., "President", "Vice President")
    that occurs within a broader election event. Each election has its own
    set of candidates and timing.
    
    Attributes:
        election_event (ForeignKey): The election event this election belongs to
        title (CharField): The name/title of the election
        description (TextField): Detailed description of the election
        start_time (DateTimeField): When voting begins for this election
        end_time (DateTimeField): When voting ends for this election
        is_active (BooleanField): Whether the election is currently active
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
        Check if the election is currently open for voting.
        
        An election is considered open if it's active and the current
        time falls within the start and end time window.
        
        Returns:
            bool: True if the election is open for voting, False otherwise
        """
        now = timezone.now()
        return self.is_active and self.start_time <= now <= self.end_time
    
    def __str__(self):
        """
        Return string representation of the election.
        
        Returns:
            str: The election title followed by the election event title
        """
        return f"{self.title} ({self.election_event.title})"
    
    def save(self, *args, **kwargs):
        """
        Set default start and end times from election_event if not provided.
        """
        if self.election_event:
            if not self.start_time:
                self.start_time = self.election_event.start_time
            if not self.end_time:
                self.end_time = self.election_event.end_time
        
        self.full_clean()
        super().save(*args, **kwargs)
    
    def clean(self):
        """
        Ensure election start and end times falls within election_event start
        and end times.
        """
        if (
            self.start_time and
            self.election_event and
            self.start_time < self.election_event.start_time
        ):
            raise ValidationError(
                "Election start time cannot be before election event start time."
            )
        if (
            self.end_time and
            self.election_event and
            self.end_time > self.election_event.end_time
        ):
            raise ValidationError(
                "Election end time cannot be after election event end time."
            )


class Candidate(BaseUUIDModel):
    """
    Candidate model representing a candidate contesting in a specific
    election within a specific election event.

    Candidate may optionally be a registered voter.
    
    Attributes:
        election (ForeignKey): The election this candidate is contesting in
        first_name (CharField): The candidate's first name
        last_name (CharField): The candidate's last name
        bio (TextField): Optional biographical information about the candidate
        user (ForeignKey): Optional link to a User account if candidate is also a voter
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
        Return string representation of the candidate.
        
        Returns:
            str: The candidate's full name followed by the election title
        """
        return f"{self.first_name} {self.last_name} ({self.election.title})"