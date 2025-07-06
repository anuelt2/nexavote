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