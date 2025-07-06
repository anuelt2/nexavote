"""
"""
from django.contrib.auth import get_user_model, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from users.serializers import RegisterViaTokenSerializer, AdminStaffRegistrationSerializer
from users.models import VoterProfile
from invitations.models import Invitation
from users.forms import VoterRegistrationForm

User = get_user_model()


class RegisterViaTokenView(APIView):
    """
    POST endpoint to register a voter via a one-time invitation token
    """
    def post(self, request):
        """
        Process voter registration via invitation token.
        
        Args:
            request (Request): The HTTP request object
        
        Returns:
            Response: Registration success or error response
        """
        serializer = RegisterViaTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                    {"message": "Voter registration successful"},
                    status=status.HTTP_201_CREATED
                    )
        return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
                )


class AdminStaffRegistrationView(APIView):
    """
    View to handle direct registration for admin and staff users.
    
    This view allows administrators to create admin and staff accounts
    without using an invitation token.
    """
    permission_classes = [permissions.IsAdminUser]  # Only admins can create admin/staff accounts

    def post(self, request):
        """
        Process admin or staff user registration.
        
        Args:
            request (Request): The HTTP request object
        
        Returns:
            Response: Registration success or error response
        """
        serializer = AdminStaffRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "Admin/Staff registration successful"},
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LogoutAnyMethodView(View):
    """
    """
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')


class RegisterViaTokenHTMLView(View):
    """
    """
    def get(self, request):
        """
        """
        if request.user.is_authenticated:
            logout(request)

        token = request.GET.get("token")
        try:
            invitation = Invitation.objects.get(token=token, is_used=False)
        except Invitation.DoesNotExist:
            return render(request, "users/register_voter.html", {"invalid_token": True})
        
        form = VoterRegistrationForm(initial={"email": invitation.email})
        return render(request, "users/register_voter.html", {"form": form})
    
    def post(self, request):
        """
        """
        token = request.GET.get("token")

        try:
            invitation = Invitation.objects.get(token=token, is_used=False)
        except Invitation.DoesNotExist:
            return render(request, "users/register_voter.html", {"invalid_token": True})
        
        form = VoterRegistrationForm(request.POST, initial={"email": invitation.email})
        
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            password = form.cleaned_data["password1"]

            user = User.objects.filter(email=invitation.email).first()

            if user is None:
                user = User.objects.create_user(
                    email=invitation.email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                    role="voter"
                )
            
            try:
                voter = user.voterprofile
            except VoterProfile.DoesNotExist:
                    voter = VoterProfile.objects.create(user=user, election_event=invitation.election_event)

            invitation.is_used = True
            invitation.save()

            login(request, user)
            return redirect("home")
        
        return render(request, "users/register_voter.html", {"form": form})
    

class VoterListView(View):
    """
    """
    @method_decorator(staff_member_required)
    def get(self, request):
        """
        """
        voters = VoterProfile.objects.select_related('user', 'election_event')
        return render(request, "users/voter_list.html", {"voters": voters})