"""
"""
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

def send_invite_email(invitation, use_api=False):
        """
        Sends an email to the invited voter with one-time use registration
        link containing the token using a text template.
        """
        base_url = getattr(settings, "FRONTEND_URL", "http://localhost:8000")
        if use_api:
            registration_url = f"{base_url}/api/register/?token={invitation.token}"
        else:
            registration_url = f"{base_url}/auth/register/voter/html?token={invitation.token}"

        context = {
            'election_title': invitation.election_event.title,
            'registration_url': registration_url,
        }
        subject = f"You are invited to register for {invitation.election_event.title}"
        message = render_to_string('emails/invitation_email.txt', context)

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [invitation.email],
            fail_silently=False,
        )