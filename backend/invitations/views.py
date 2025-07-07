"""
"""
from django.views import View
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator

from rest_framework import generics, permissions, status

from .forms import InvitationForm
from invitations.models import Invitation
from invitations.serializers import InvitationCreateSerializer
from invitations.utils import send_invite_email

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .forms import CSVUploadForm
from .services import CSVInvitationService
from elections.models import ElectionEvent
from users.permissions import IsElectionAdmin


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


@method_decorator(staff_member_required, name='dispatch')
class CSVUploadView(View):
    """
    View for uploading CSV files with voter information.
    """
    template_name = 'invitations/csv_upload.html'
    
    def get(self, request, event_id):
        """
        Display CSV upload form.
        """
        election_event = get_object_or_404(ElectionEvent, id=event_id)
        form = CSVUploadForm()
        
        return render(request, self.template_name, {
            'form': form,
            'election_event': election_event,
        })
    
    def post(self, request, event_id):
        """
        Process CSV upload and create invitations.
        """
        election_event = get_object_or_404(ElectionEvent, id=event_id)
        form = CSVUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            service = CSVInvitationService(request)
            
            try:
                results = service.process_csv_upload(csv_file, election_event)
                
                # Add success message
                messages.success(
                    request,
                    f"CSV processed successfully! "
                    f"Invitations sent: {results['successful_invitations']}, "
                    f"Failed: {results['failed_invitations']}, "
                    f"Duplicates: {results['duplicate_emails']}"
                )
                
                # Store results in session for display
                request.session['csv_results'] = results
                
                return redirect('invitations:csv-results', event_id=event_id)
                
            except Exception as e:
                messages.error(request, f"Error processing CSV: {str(e)}")
        
        return render(request, self.template_name, {
            'form': form,
            'election_event': election_event,
        })


@method_decorator(staff_member_required, name='dispatch')
class CSVResultsView(View):
    """
    View for displaying CSV upload results.
    """
    template_name = 'invitations/csv_results.html'
    
    def get(self, request, event_id):
        """
        Display CSV upload results.
        """
        election_event = get_object_or_404(ElectionEvent, id=event_id)
        results = request.session.get('csv_results', {})
        
        # Clear results from session
        if 'csv_results' in request.session:
            del request.session['csv_results']
        
        return render(request, self.template_name, {
            'election_event': election_event,
            'results': results,
        })


class CSVUploadAPIView(APIView):
    """
    API endpoint for uploading CSV files.
    """
    permission_classes = [permissions.IsAuthenticated, IsElectionAdmin]
    
    def post(self, request, event_id):
        """
        Process CSV upload via API.
        """
        election_event = get_object_or_404(ElectionEvent, id=event_id)
        
        if 'csv_file' not in request.FILES:
            return Response(
                {'error': 'No CSV file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        csv_file = request.FILES['csv_file']
        form = CSVUploadForm({'csv_file': csv_file})
        
        if form.is_valid():
            service = CSVInvitationService(request)
            
            try:
                results = service.process_csv_upload(csv_file, election_event)
                return Response(results, status=status.HTTP_200_OK)
                
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(
            {'error': 'Invalid CSV file', 'details': form.errors},
            status=status.HTTP_400_BAD_REQUEST
        )