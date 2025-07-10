"""
"""
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

def send_password_reset_email(request, user):
        """
        Sends an email to newly created admin/staff user to reset account password.
        """
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        domain = get_current_site(request).domain
        reset_link = f"http://{domain}/auth/reset/{uid}/{token}"

        context = {
            'user': user,
            'reset_link': reset_link,
        }

        subject = "Reset Your NexaVote Password"
        message = render_to_string('emails/admin_set_password.txt', context)

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

def send_voter_registration_email(user, election_event):
        """
        Sends registration confirmation email to voter.
        """
        subject = "Welcome to Nexavote - Registration Successful"

        message = f"""
Hello {user.first_name},

You have successfully registered as a voter for the election event:
{election_event.title}.

You can now log in and particpate in any elections available within this event.

If you did not request this registration, please contact our support team immediately.

Thank you,
The NexaVote Team
""".strip()
        
        send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
        )