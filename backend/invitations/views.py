"""
Django views for invitation management.

This module contains view classes for creating and managing voter invitations
via both API and HTML interfaces, including bulk invitation functionality.
"""
import csv
from io import TextIOWrapper

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from election_events.models import ElectionEvent
from invitations.forms import InvitationForm
from invitations.models import Invitation
from invitations.serializers import (
    InvitationCreateSerializer,
    InvitationListSerializer,
    CSVUploadSerializer
)
from invitations.utils import send_invite_email
from users.permissions import IsElectionAdmin


# === API Views ===

class InvitationCreateAPIView(generics.CreateAPIView):
    """
    API view for creating individual voter invitations.
    
    Allows admin users to create voter invitations via API endpoint
    with automatic email sending upon successful creation.
    
    Permissions:
        - IsAdminUser: Only admin users can create invitations
        
    Methods:
        POST: Create a new invitation and send invitation email
    """
    queryset = Invitation.objects.all()
    serializer_class = InvitationCreateSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def perform_create(self, serializer):
        """
        Handle invitation creation and send email notification.
        
        Saves the invitation instance and triggers the invitation email
        sending process.
        
        Args:
            serializer: The validated serializer instance containing invitation data
        """
        invitation = serializer.save()
        send_invite_email(invitation, use_api=True)


class InvitationListCreateView(generics.ListCreateAPIView):
    """
    API view for listing all invitations and creating new ones.
    
    Provides endpoints for both retrieving all invitations and creating
    new invitation instances.
    
    Permissions:
        - IsAdminUser: Only admin users can access this endpoint
        
    Methods:
        GET: Retrieve list of all invitations
        POST: Create a new invitation
    """
    queryset = Invitation.objects.all()
    serializer_class = InvitationListSerializer
    permission_classes = [permissions.IsAdminUser]


class InvitationDetailView(generics.RetrieveAPIView):
    """
    API view for retrieving individual invitation details.
    
    Provides read-only access to specific invitation information
    by invitation ID.
    
    Permissions:
        - IsAdminUser: Only admin users can access invitation details
        
    Methods:
        GET: Retrieve specific invitation details
    """
    queryset = Invitation.objects.all()
    serializer_class = InvitationListSerializer
    permission_classes = [permissions.IsAdminUser]


class InvitationsByEventView(generics.ListAPIView):
    """
    API view for retrieving invitations filtered by election event.
    
    Returns all invitations associated with a specific election event,
    useful for managing invitations per event.
    
    URL Parameters:
        event_id: UUID of the election event
        
    Methods:
        GET: Retrieve invitations for specified election event
    """
    serializer_class = InvitationListSerializer

    def get_queryset(self):
        """
        Filter invitations by election event ID from URL parameters.
        
        Returns:
            QuerySet: Invitations filtered by election event ID
        """
        event_id = self.kwargs['event_id']
        return Invitation.objects.filter(election_event_id=event_id)


class InvitationMarkUsedView(APIView):
    """
    API view for marking invitations as used.
    
    Allows administrators to manually mark invitations as used,
    preventing further use of the invitation token.
    
    Methods:
        PATCH: Mark invitation as used
    """
    
    def patch(self, request, pk):
        """
        Mark an invitation as used.
        
        Updates the invitation's is_used flag to True, preventing
        the invitation from being used for registration.
        
        Args:
            request: The HTTP request object
            pk: Primary key of the invitation to mark as used
            
        Returns:
            Response: Success message or error if invitation already used
        """
        invitation = get_object_or_404(Invitation, pk=pk)
        if invitation.is_used:
            return Response(
                {'detail': 'Invitation already marked as used.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        invitation.is_used = True
        invitation.save()
        return Response(
            {'detail': 'Invitation marked as used.'}, 
            status=status.HTTP_200_OK
        )


class InvitationByTokenView(generics.RetrieveAPIView):
    """
    API view for retrieving invitation details by token.
    
    Allows retrieval of invitation information using the invitation token,
    typically used during the registration process to verify invitation validity.
    
    URL Parameters:
        token: UUID token of the invitation
        
    Methods:
        GET: Retrieve invitation details by token
    """
    serializer_class = InvitationListSerializer
    lookup_field = 'token'
    queryset = Invitation.objects.all()


# === Template Views ===

@method_decorator(staff_member_required, name='dispatch')
class InvitationCreateView(View):
    """
    HTML view for creating voter invitations through web interface.
    
    Provides a form-based interface for staff members to create individual
    voter invitations with validation and email sending.
    
    Decorators:
        staff_member_required: Restricts access to staff members only
    """
    
    def get(self, request):
        """
        Display the invitation creation form.
        
        Args:
            request: The HTTP request object
            
        Returns:
            HttpResponse: Rendered invitation creation form
        """
        form = InvitationForm()
        return render(request, "invitations/invite.html", {"form": form})
    
    def post(self, request):
        """
        Process invitation creation form submission.
        
        Validates form data, checks for duplicate invitations, creates
        new invitation, and sends invitation email.
        
        Args:
            request: The HTTP request object containing form data
            
        Returns:
            HttpResponse: Success redirect or form with validation errors
        """
        form = InvitationForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            election_event = form.cleaned_data['election_event']
            
            # Check for existing unused invitation
            existing_invitation = Invitation.objects.filter(
                email=email,
                election_event=election_event,
                is_used=False
            ).first()
            
            if existing_invitation:
                messages.warning(
                    request, 
                    f"An unused invitation has already been sent to {email} for this election."
                )
                return render(request, "invitations/invite.html", {"form": form})
            
            # Create and save new invitation
            invitation = form.save(commit=False)
            invitation.save()
            send_invite_email(invitation, use_api=False)
            return redirect("voter-list")
        else:
            messages.error(request, "Error with submission. Please check form and try again.")
            return render(request, "invitations/invite.html", {"form": form})


class BulkInviteUploadAPIView(generics.GenericAPIView):
    """
    API view for bulk invitation creation via CSV upload.
    
    Processes CSV files containing email addresses to create multiple
    invitations simultaneously for a specified election event.
    
    Permissions:
        - IsAuthenticated: User must be authenticated
        - IsElectionAdmin: User must have election admin privileges
        
    Methods:
        POST: Upload CSV file and create bulk invitations
    """
    serializer_class = CSVUploadSerializer
    permission_classes = [permissions.IsAuthenticated, IsElectionAdmin]

    def post(self, request):
        """
        Process CSV file upload and create bulk invitations.
        
        Validates the uploaded CSV file, extracts email addresses,
        creates invitations for each email, and sends invitation emails.
        
        Args:
            request: HTTP request containing CSV file and election event ID
            
        Returns:
            Response: Summary of sent and skipped invitations with counts
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        file = serializer.validated_data['file']
        election_event_id = serializer.validated_data['election_event_id']

        # Validate election event exists
        try:
            election_event = ElectionEvent.objects.get(id=election_event_id)
        except ElectionEvent.DoesNotExist:
            return Response(
                {"election_event_id": "Invalid election event ID."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Process CSV file
        csv_file = TextIOWrapper(file.file, encoding='utf-8')
        reader = csv.reader(csv_file)

        emails = set()
        for row in reader:
            if row:
                email = row[0].strip().lower()
                if email:
                    emails.add(email)
        
        # Create invitations
        sent = []
        skipped = []

        for email in emails:
            if Invitation.objects.filter(email=email, election_event=election_event).exists():
                skipped.append(email)
                continue

            invitation = Invitation.objects.create(email=email, election_event=election_event)
            send_invite_email(invitation)
            sent.append(email)

        return Response({
            "sent": sent,
            "skipped": skipped,
            "sent_count": len(sent),
            "skipped_count": len(skipped),
            "election_event": election_event_id
        }, status=status.HTTP_201_CREATED)
