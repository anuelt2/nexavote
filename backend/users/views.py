"""
Django views module for user registration and authentication.

This module contains view classes for handling user registration via invitation tokens,
admin/staff registration, logout functionality, and voter management.
"""
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from invitations.models import Invitation
from users.forms import VoterRegistrationForm
from users.models import VoterProfile
from users.serializers import RegisterViaTokenSerializer, CurrentUserSerializer


User = get_user_model()


# === API Views ===

class RegisterViaTokenView(APIView):
    """
    API endpoint to register a voter via a one-time invitation token.
    """
    permission_classes = [permissions.AllowAny]
    
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


class LoginAPIView(APIView):
    """
    """
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(APIView):
    """
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except Exception:
            pass
        return Response({"detail": "Logged out successfully."}, status=status.HTTP_200_OK)


class CurrentUserView(APIView):
    """
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        """
        serializer = CurrentUserSerializer(request.user)
        return Response(serializer.data)


# class AdminStaffRegistrationView(APIView):
#     """
#     API view to handle direct registration for admin and staff users.
    
#     This view allows administrators to create admin and staff accounts
#     without using an invitation token.
#     """
#     permission_classes = [permissions.IsAdminUser]
    
#     def post(self, request):
#         """
#         Process admin or staff user registration.
        
#         Args:
#             request (Request): The HTTP request object
        
#         Returns:
#             Response: Registration success or error response
#         """
#         serializer = AdminStaffRegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response(
#                 {"message": "Admin/Staff registration successful"},
#                 status=status.HTTP_201_CREATED
#             )
#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )


# === Template Views ===

class LoginView(LoginView):
    """
    Custom login view.
    Redirects authenticated users away from login page
    """
    template_name = "registration/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.is_staff:
            return reverse('admin-elections')
        else:
            return reverse('election-list')


class LogoutView(View):
    """
    View to handle logout for any HTTP method and redirect to home.
    """
    def dispatch(self, request, *args, **kwargs):
        """
        Handle logout for any HTTP method.
        
        Args:
            request: The HTTP request object
            *args: Variable positional arguments
            **kwargs: Variable keyword arguments
            
        Returns:
            HttpResponseRedirect: Redirect to home page
        """
        logout(request)
        return redirect('home')


class RegisterViaTokenHTMLView(View):
    """
    HTML view to handle voter registration via invitation token.
    
    Provides GET and POST methods to display and process the voter
    registration form using invitation tokens.
    """
    def get(self, request):
        """
        Display voter registration form with token validation.
        
        Args:
            request: The HTTP request object
            
        Returns:
            HttpResponse: Registration form or error page
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
        Process voter registration form submission.
        
        Args:
            request: The HTTP request object
            
        Returns:
            HttpResponse: Success redirect or form with errors
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
    View to display a list of all voters (staff access required).
    """
    @method_decorator(staff_member_required)
    def get(self, request):
        """
        Display list of all voters with their election events.
        
        Args:
            request: The HTTP request object
            
        Returns:
            HttpResponse: Voter list page
        """
        voters = VoterProfile.objects.select_related('user', 'election_event')
        return render(request, "users/voter_list.html", {"voters": voters})

