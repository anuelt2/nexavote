"""
"""
from django.views import View
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

from rest_framework import generics, permissions

from invitations.forms import InvitationForm
from invitations.models import Invitation
from invitations.serializers import InvitationCreateSerializer
from invitations.utils import send_invite_email


class InvitationCreateAPIView(generics.CreateAPIView):
    """
    """
    queryset = Invitation.objects.all()
    serializer_class = InvitationCreateSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        """
        """
        invitation = serializer.save()
        send_invite_email(invitation, use_api=True)


class InvitationCreateView(View):
    """
    """
    @method_decorator(staff_member_required)
    def get(self, request):
        """
        """
        form = InvitationForm()
        return render(request, "invitations/invite.html", {"form": form})
    
    @method_decorator(staff_member_required)
    def post(self, request):
        """
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
                return render(request, "invitations/invite.html"), {"form": form}

            invitation = form.save(commit=False)
            invitation.save()
            send_invite_email(invitation, use_api=False)
            return redirect("voter-list")
        else:
            messages.error(request, "Error with submission. Please check form and try again.")
            empty_form = InvitationForm()
            return render(request, "invitations/invite.html", {"form": empty_form})