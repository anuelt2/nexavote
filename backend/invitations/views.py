"""
Django views for invitation management.

This module contains view classes for creating and managing voter invitations
via both API and HTML interfaces.
"""
import csv
from io import TextIOWrapper

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from rest_framework import generics, permissions, status
<<<<<<< HEAD

from .forms import InvitationForm
=======
from rest_framework.response import Response
from rest_framework.views import APIView

from election_events.models import ElectionEvent
from invitations.forms import InvitationForm
>>>>>>> 4687d895cc677049e99de1fe092309922a2483b8
from invitations.models import Invitation
from invitations.serializers import (
    InvitationCreateSerializer,
    InvitationListSerializer,
    CSVUploadSerializer
)
from invitations.utils import send_invite_email
from users.permissions import IsElectionAdmin

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .forms import CSVUploadForm
from .services import CSVInvitationService
from elections.models import ElectionEvent
from users.permissions import IsElectionAdmin


# === API Views ===

class InvitationCreateAPIView(generics.CreateAPIView):
    """
    API view for creating voter invitations.
    
    Allows admin users to create invitations via API endpoint.
    """
    queryset = Invitation.objects.all()
    serializer_class = InvitationCreateSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def perform_create(self, serializer):
        """
        Handle invitation creation and send email notification.
        
        Args:
            serializer: The validated serializer instance
        """
        invitation = serializer.save()
        send_invite_email(invitation, use_api=True)


class InvitationListCreateView(generics.ListCreateAPIView):
    """
    """
    queryset = Invitation.objects.all()
    serializer_class = InvitationListSerializer
    permission_classes = [permissions.IsAdminUser]


class InvitationDetailView(generics.RetrieveAPIView):
    """
    """
    queryset = Invitation.objects.all()
    serializer_class = InvitationListSerializer
    permission_classes = [permissions.IsAdminUser]


class InvitationsByEventView(generics.ListAPIView):
    """
    """
    serializer_class = InvitationListSerializer

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        return Invitation.objects.filter(election_event_id=event_id)


class InvitationMarkUsedView(APIView):
    """
    """
    def patch(self, request, pk):
        invitation = get_object_or_404(Invitation, pk=pk)
        if invitation.is_used:
            return Response({'detail': 'Invitation already marked as used.'}, status=status.HTTP_404_BAD_REQUEST)
        
        invitation.is_used = True
        invitation.save()
        return Response({'detail': 'Invitation marked as used.'}, status=status.HTTP_200_OK)


class InvitationByTokenView(generics.RetrieveAPIView):
    """
    Get and verify inivitaiton details via token before registration proceeds.
    """
    serializer_class = InvitationListSerializer
    lookup_field = 'token'
    queryset = Invitation.objects.all()


# === Template Views ===

@method_decorator(staff_member_required, name='dispatch')
class InvitationCreateView(View):
    """
    HTML view for creating voter invitations.
    
    Provides form-based interface for staff members to create invitations.
    """
    def get(self, request):
        """
        Display invitation creation form.
        
        Args:
            request: The HTTP request object
            
        Returns:
            HttpResponse: Invitation form page
        """
        form = InvitationForm()
        return render(request, "invitations/invite.html", {"form": form})
    
    def post(self, request):
        """
        Process invitation creation form submission.
        
        Args:
            request: The HTTP request object
            
        Returns:
            HttpResponse: Success redirect or form with errors
        """
        form = InvitationForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            election_event = form.cleaned_data['election_event']
            
            existing_invitation = Invitation.objects.filter(
                email=email,
                election_event=election_event,
                is_used=False
            ).first()
            
            if existing_invitation:
                messages.warning(request, f"An unused invitation has already been sent to {email} for this election.")
                return render(request, "invitations/invite.html", {"form": form})
            
            invitation = form.save(commit=False)
            invitation.save()
            send_invite_email(invitation, use_api=False)
            return redirect("voter-list")
        else:
            messages.error(request, "Error with submission. Please check form and try again.")
            empty_form = InvitationForm()
            return render(request, "invitations/invite.html", {"form": form})


class BulkInviteUploadAPIView(generics.GenericAPIView):
    """
    """
    serializer_class = CSVUploadSerializer
    permission_classes = [permissions.IsAuthenticated, IsElectionAdmin]

    def post(self, request):
        """
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        file = serializer.validated_data['file']
        election_event_id = serializer.validated_data['election_event_id']

        try:
            election_event = ElectionEvent.objects.get(id=election_event_id)
        except ElectionEvent.DoesNotExist:
            return Response({"election_event_id": "Invalid election event ID."}, status=status.HTTP_400_BAD_REQUEST)

        csv_file = TextIOWrapper(file.file, encoding='utf-8')
        reader = csv.reader(csv_file)

        emails = set()

        for row in reader:
            if row:
                email = row[0].strip().lower()
                if email:
                    emails.add(email)
        
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
