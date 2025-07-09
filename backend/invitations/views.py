"""
Django views for invitation management.

This module contains view classes for creating and managing voter invitations
via both API and HTML interfaces.
"""
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from invitations.forms import InvitationForm
from invitations.models import Invitation
from invitations.serializers import InvitationCreateSerializer, InvitationListSerializer
from invitations.utils import send_invite_email


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
