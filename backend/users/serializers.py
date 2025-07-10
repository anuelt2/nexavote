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
    Register user via invitation token.
    """
    token = serializers.UUIDField()
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)

    def validate_token(self, value):
        """
        Checks that invitation token is valid and unused.
        """
        if not Invitation.objects.filter(token=value, is_used=False).exists():
            raise serializers.ValidationError("Invalid or expired token")
        return value

    def create(self, validated_data):
        """
        Create a new voter user and associated voter profile.

        Args:
            validated_data (dict): Validated registration data

        Returns:
            User: The newly created voter user
        """
        token = validated_data["token"]
        invitation = Invitation.objects.get(token=token, is_used=False)
        password = validated_data["password"]
        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]
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

        if created:
            user.set_password(password)
            user.save()
        
        if VoterProfile.objects.filter(user=user, election_event=election_event).exists():
            raise serializers.validationError("You are already registered as a voter for this election event.")

        VoterProfile.objects.create(user=user, election_event=invitation.election_event)

        invitation.is_used = True
        invitation.save()

        return user


class CurrentUserSerializer(serializers.ModelSerializer):
    """
    """
    voter_profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_staff', 'voter_profile']
    
    def get_voter_profile(self,obj):
        try:
            profile = obj.voterprofile
            return {
                'id': str(profile.id),
                'election_event': profile.election_event.title
            }
        except VoterProfile.DoesNotExist:
            return None


# class AdminStaffRegistrationSerializer(serializers.ModelSerializer):
#     """
#     Serializer for direct registration of admin and staff users.

#     This serializer allows admins and staff to register directly,
#     without requiring an invitation token.
#     """
#     class Meta:
#         model = User
#         fields = ["email", "first_name", "last_name", "password", "role"]
#         extra_kwargs = {"password": {"write_only": True}, "role": {"required": True}}

#     def validate_role(self, value):
#         """
#         Validate that only admin or staff roles can be registered directly.

#         Args:
#             value (str): The proposed user role

#         Returns:
#             str: The validated role

#         Raises:
#             ValidationError: If an invalid role is specified
#         """
#         if value not in ["admin", "staff"]:
#             raise serializers.ValidationError(
#                 "Only admin and staff roles are allowed."
#             )
#         return value

    # def create(self, validated_data):
    #     """
    #     Create a new admin or staff user.

    #     Args:
    #         validated_data (dict): Validated registration data

    #     Returns:
    #         User: The newly created admin or staff user
    #     """
    #     role = validated_data['role']
    #     is_staff = role in ['admin', 'staff']

    #     user = User.objects.create_user(
    #         email=validated_data['email'],
    #         password=validated_data['password'],
    #         first_name=validated_data['first_name'],
    #         last_name=validated_data['last_name'],
    #         role=role,
    #         is_staff=is_staff,
    #         is_superuser=(role == 'admin'),
    #     )
    #     return user


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    """
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
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
        """
        password = self.validated_data['new_password']
        self.user.set_password(password)
        self.user.save()
        return self.user


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    """
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("No user with this email exists.")
        
        if not user.is_active:
            raise serializers.ValidationError("User account is inactive.")
        
        self.context['user'] = user
        return value