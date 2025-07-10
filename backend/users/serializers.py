"""
Django REST Framework serializers for user registration.

This module contains serializers for handling user registration via invitation tokens
and direct admin/staff registration.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from rest_framework import serializers

from invitations.models import Invitation
from users.models import User, VoterProfile

User = get_user_model()


class RegisterViaTokenSerializer(serializers.Serializer):
    """
    Serializer for registering users via invitation token.
    
    Handles voter registration through invitation tokens, validating the token
    and creating both User and VoterProfile instances upon successful registration.
    
    Attributes:
        token (UUIDField): The invitation token UUID
        first_name (CharField): User's first name (max 50 characters)
        last_name (CharField): User's last name (max 50 characters)
        password (CharField): User's password (write-only)
    """
    token = serializers.UUIDField(
        help_text="Valid invitation token UUID for voter registration"
    )
    first_name = serializers.CharField(
        max_length=50,
        help_text="User's first name"
    )
    last_name = serializers.CharField(
        max_length=50,
        help_text="User's last name"
    )
    password = serializers.CharField(
        write_only=True,
        help_text="User's password for account creation"
    )

    def validate_token(self, value):
        """
        Validate that the invitation token is valid and unused.
        
        Args:
            value (UUID): The invitation token to validate
            
        Returns:
            UUID: The validated token
            
        Raises:
            ValidationError: If token is invalid or already used
        """
        if not Invitation.objects.filter(token=value, is_used=False).exists():
            raise serializers.ValidationError("Invalid or expired token")
        return value

    def create(self, validated_data):
        """
        Create a new voter user and associated voter profile.

        Args:
            validated_data (dict): Validated registration data containing
                token, first_name, last_name, and password

        Returns:
            User: The newly created voter user instance
            
        Raises:
            ValidationError: If user is already registered for the election event
        """
        token = validated_data["token"]
        invitation = Invitation.objects.get(token=token, is_used=False)
        password = validated_data["password"]
        first_name = validated_data["first_name"].strip()
        last_name = validated_data["last_name"].strip()
        email = invitation.email
        election_event = invitation.election_event

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "role": "voter",
            }
        )

        updated = False
        if not created:
            if not user.first_name and first_name:
                user.first_name = first_name
                updated = True
            if not user.last_name and last_name:
                user.last_name = last_name
                updated = True
            if updated:
                user.save()

        if created:
            user.set_password(password)
            user.save()
        
        if VoterProfile.objects.filter(user=user, election_event=election_event).exists():
            raise serializers.ValidationError("You are already registered as a voter for this election event.")

        VoterProfile.objects.create(user=user, election_event=invitation.election_event)

        invitation.is_used = True
        invitation.save()

        return user


class CurrentUserSerializer(serializers.ModelSerializer):
    """
    Serializer for current authenticated user information.
    
    Provides user details including associated voter profile information
    for the currently authenticated user.
    
    Fields:
        id: User's unique identifier
        email: User's email address
        first_name: User's first name
        last_name: User's last name
        is_staff: Boolean indicating staff status
        voter_profile: Associated voter profile details (if exists)
    """
    voter_profile = serializers.SerializerMethodField(
        help_text="Associated voter profile information including election event details"
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_staff', 'voter_profile']
    
    def get_voter_profile(self, obj):
        """
        Retrieve voter profile information for the user.
        
        Args:
            obj (User): The user instance
            
        Returns:
            dict or None: Dictionary containing voter profile ID and election event title,
                         or None if no voter profile exists
        """
        try:
            profile = obj.voterprofile
            return {
                'id': str(profile.id),
                'election_event': profile.election_event.title
            }
        except VoterProfile.DoesNotExist:
            return None


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming password reset with token validation.
    
    Handles the final step of password reset process where users provide
    the reset token and new password.
    
    Attributes:
        uid (CharField): Base64 encoded user ID
        token (CharField): Password reset token
        new_password (CharField): New password to set (write-only)
    """
    uid = serializers.CharField(
        help_text="Base64 encoded user ID from password reset email"
    )
    token = serializers.CharField(
        help_text="Password reset token from reset email"
    )
    new_password = serializers.CharField(
        write_only=True,
        help_text="New password to set for the user account"
    )

    def validate(self, data):
        """
        Validate the password reset token and user ID.
        
        Args:
            data (dict): Dictionary containing uid, token, and new_password
            
        Returns:
            dict: Validated data
            
        Raises:
            ValidationError: If user ID is invalid or token is expired/invalid
        """
        try:
            uid = force_str(urlsafe_base64_decode(data['uid']))
            self.user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            raise serializers.ValidationError({'uid': 'Invalid user ID'})
        
        if not default_token_generator.check_token(self.user, data['token']):
            raise serializers.ValidationError({'token': 'Invalid or expired token'})
        
        validate_password(data['new_password'], self.user)
        return data
    
    def save(self):
        """
        Save the new password for the user.
        
        Returns:
            User: The user instance with updated password
        """
        password = self.validated_data['new_password']
        self.user.set_password(password)
        self.user.save()
        return self.user


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for requesting password reset via email.
    
    Validates the email address and ensures the user exists and is active
    before initiating the password reset process.
    
    Attributes:
        email (EmailField): Email address of the user requesting password reset
    """
    email = serializers.EmailField(
        help_text="Email address of the user requesting password reset"
    )

    def validate_email(self, value):
        """
        Validate that the email belongs to an active user.
        
        Args:
            value (str): Email address to validate
            
        Returns:
            str: Validated email address
            
        Raises:
            ValidationError: If no user exists with the email or user is inactive
        """
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("No user with this email exists.")
        
        if not user.is_active:
            raise serializers.ValidationError("User account is inactive.")
        
        self.context['user'] = user
        return value

