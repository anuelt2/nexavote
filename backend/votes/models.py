"""
votes/models.py

This module defines the Vote model for recording and managing votes
cast by voters in elections.

The Vote model ensures one vote per voter per election and maintains
vote integrity and anonymity.
"""
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from core.models import BaseUUIDModel
from elections.models import Election
from users.models import VoterProfile


class Vote(BaseUUIDModel):
    """
    Vote model representing a vote cast by a voter in a specific election.
    
    This model ensures:
    - One vote per voter per election
    - Vote integrity and auditability
    - Voter anonymity (no direct link to specific voter choice)
    """

    election = models.ForeignKey(
        Election,
        on_delete=models.CASCADE,
        related_name='votes'
    )
    voter = models.ForeignKey(
        VoterProfile,
        on_delete=models.CASCADE,
        related_name='votes'
    )
    vote_choice = models.TextField()
    date_and_time = models.DateTimeField(auto_now_add=True)
    encrypted_vote = models.TextField(blank=True, null=True) #Encrypts vote_choise for additional security
    vote_hash = models.CharField(max_length=64, blank=True)
    is_verified = models.BooleanField(default=True)

    
    class Meta:
        """
        Ensures one vote per voter per election
        """
        unique_together = ['election', 'voter']
        ordering = ['date_and_time']
        indexes = [
            models.Index(fields=['election', 'date_and_time']),
            models.Index(fields=['voter', 'date_and_time']),
        ]
    
    def clean(self):
        """
        Validates the vote before saving to database.
        """
        super().clean()
        
        if not self.election.is_open():
            raise ValidationError(
                'Cannot cast vote: Election is not currently open.'
            )
        
        if not self._is_voter_eligible():
            raise ValidationError(
                'Voter is not eligible for this election event.'
            )
    
    def _is_voter_eligible(self):
        """
        Check if the voter is eligible to vote in this election's event.
        
        Returns:
            bool: True if voter is eligible, False otherwise.
        """
        return self.election.election_event.invitations.filter(
            email=self.voter.user.email,
            is_used=True
        ).exists()
    
    def save(self, *args, **kwargs):
        """
        Override save to perform validation and generate vote hash.
        """
        self.full_clean()
        if not self.vote_hash:
            self.vote_hash = self._generate_vote_hash()
        
        super().save(*args, **kwargs)
    
    def _generate_vote_hash(self):
        """
        Generate a hash for vote integrity verification.
        
        Returns:
            str: SHA-256 hash of vote data.
        """
        import hashlib
        
        vote_data = f"{self.election.id}{self.voter.id}{self.vote_choice}{timezone.now().isoformat()}"
        return hashlib.sha256(vote_data.encode()).hexdigest()
    
    def __str__(self):
        """
        Return string representation of the vote.
        """
        return f"Vote by {self.voter.user.email} in {self.election.title}"
    
    @classmethod
    def get_election_results(cls, election):
        """
        Get vote count results for a specific election.
        
        Args:
            election: Election instance
            
        Returns:
            dict: Vote counts by choice
        """
        votes = cls.objects.filter(election=election, is_verified=True)
        results = {}
        
        for vote in votes:
            choice = vote.vote_choice
            results[choice] = results.get(choice, 0) + 1
        
        return results
    
    @classmethod
    def get_voter_participation(cls, election_event):
        """
        Get voter participation statistics for an election event.
        
        Args:
            election_event: ElectionEvent instance
            
        Returns:
            dict: Participation statistics
        """
        from django.db.models import Count, Q
        
        elections = election_event.elections.all()
        voted_voters = cls.objects.filter(
            election__in=elections
        ).values('voter').distinct().count()
        total_invited = election_event.invitations.filter(is_used=True).count()

        votes_per_election = {}
        for election in elections:
            votes_per_election[election.title] = cls.objects.filter(
                election=election,
                is_verified=True
            ).count()
        
        return {
            'total_invited_voters': total_invited,
            'unique_voters_participated': voted_voters,
            'participation_rate': (voted_voters / total_invited * 100) if total_invited > 0 else 0,
            'votes_per_election': votes_per_election,
            'total_votes_cast': sum(votes_per_election.values())
        }


class VoteAuditLog(BaseUUIDModel):
    """
    Audit log for tracking vote-related actions for security and transparency.
    """
    
    ACTION_CHOICES = [
        ('cast', 'Vote Cast'),
        ('modified', 'Vote Modified'),
        ('verified', 'Vote Verified'),
        ('flagged', 'Vote Flagged'),
    ]
    
    vote = models.ForeignKey(
        Vote,
        on_delete=models.CASCADE,
        related_name='audit_logs'
    )
    
    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES
    )
    
    performed_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    details = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        """
        Return string representation of the audit log entry.
        """
        return f"{self.action} - Vote {self.vote.id} at {self.timestamp}"
