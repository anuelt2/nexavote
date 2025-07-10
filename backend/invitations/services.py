import csv
import io
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from .models import Invitation
from elections.models import ElectionEvent
import logging

logger = logging.getLogger(__name__)

class CSVInvitationService:
    """
    Service class for handling CSV upload and invitation processing.
    """
    
    def __init__(self, request):
        self.request = request
        self.domain = get_current_site(request).domain
    
    def process_csv_upload(self, csv_file, election_event):
        """
        Process CSV file and create invitations.
        
        Args:
            csv_file: Uploaded CSV file
            election_event: ElectionEvent instance
            
        Returns:
            dict: Processing results
        """
        try:
            # Read CSV content
            csv_file.seek(0)
            content = csv_file.read().decode('utf-8')
            csv_reader = csv.DictReader(io.StringIO(content))
            
            results = {
                'total_rows': 0,
                'successful_invitations': 0,
                'failed_invitations': 0,
                'duplicate_emails': 0,
                'errors': []
            }
            
            with transaction.atomic():
                for row_num, row in enumerate(csv_reader, start=2):  # Start from 2 (header is row 1)
                    results['total_rows'] += 1
                    
                    try:
                        # Extract and clean data
                        first_name = row['first_name'].strip()
                        last_name = row['last_name'].strip()
                        email = row['email'].strip().lower()
                        
                        # Validate required fields
                        if not all([first_name, last_name, email]):
                            results['failed_invitations'] += 1
                            results['errors'].append(
                                f"Row {row_num}: Missing required fields"
                            )
                            continue
                        
                        # Check for duplicate email in this election event
                        if Invitation.objects.filter(
                            email=email, 
                            election_event=election_event
                        ).exists():
                            results['duplicate_emails'] += 1
                            results['errors'].append(
                                f"Row {row_num}: Email {email} already invited"
                            )
                            continue
                        
                        # Create invitation
                        invitation = Invitation.objects.create(
                            email=email,
                            first_name=first_name,
                            last_name=last_name,
                            election_event=election_event,
                            invited_by=self.request.user
                        )
                        
                        # Send invitation email
                        if self.send_invitation_email(invitation):
                            results['successful_invitations'] += 1
                        else:
                            results['failed_invitations'] += 1
                            results['errors'].append(
                                f"Row {row_num}: Failed to send email to {email}"
                            )
                    
                    except Exception as e:
                        results['failed_invitations'] += 1
                        results['errors'].append(
                            f"Row {row_num}: {str(e)}"
                        )
                        logger.error(f"Error processing row {row_num}: {str(e)}")
            
            return results
            
        except Exception as e:
            logger.error(f"Error processing CSV upload: {str(e)}")
            raise
    
    def send_invitation_email(self, invitation):
        """
        Send invitation email to a voter.
        
        Args:
            invitation: Invitation instance
            
        Returns:
            bool: True if email sent successfully
        """
        try:
            # Generate registration link
            registration_link = f"http://{self.domain}/auth/register/voter/html/?token={invitation.token}"
            
            # Email context
            context = {
                'first_name': invitation.first_name,
                'last_name': invitation.last_name,
                'election_event': invitation.election_event,
                'registration_link': registration_link,
                'domain': self.domain,
            }
            
            # Render email content
            subject = f"Invitation to Vote - {invitation.election_event.title}"
            html_message = render_to_string('emails/voter_invitation.html', context)
            plain_message = render_to_string('emails/voter_invitation.txt', context)
            
            # Send email
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[invitation.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to send invitation email to {invitation.email}: {str(e)}")
            return False
