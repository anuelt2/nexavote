"""
Email utilities for  vote receipt.

This module contains utility functions for sending emails of vote receipts
to voters with details about their vote.
"""
from django.core.mail import send_mail
from django.conf import settings

def send_vote_receipt_email(vote):
        """
        Sends a vote receipt email to the voter right after casting a
        vote with details about their vote.
        """
        email = vote.voter.user.email
        subject = f"Your Vote Receipt for {vote.election.title}"

        message = f"""
Hello {vote.voter.user.first_name},

Thank you for voting in '{vote.election.title}'.

You voted for:
- Candidate: {vote.candidate.first_name} {vote.candidate.last_name}
- Election: {vote.election.title}
- Time: {vote.created_at.strftime('%Y-%M-%d %H:%M:%S')}
- Vote Receipt Hash: {vote.vote_hash}

Keep this receipt for your records.

Regards,
NexaVote Team
""".strip()
        
        send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
        )