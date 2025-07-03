"""
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model

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
        try:
            invitation = Invitation.objects.get(token=value, is_used=False)
        except Invitation.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired token.")
        return invitation

    # def validate(self, data):
        """
        Additional validation to ensure only voter registrations are processed.

        Args:
            data (dict): The serializer data

        Returns:
            dict: Validated data

        Raises:
            ValidationError: If attempting to register a non-voter role
        """
        # invitation = data.get("token")
        # if invitation:
            # Explicitly prevent admin/staff registration via token
            # if invitation.election_event.role in ["admin", "staff"]:
                # raise serializers.ValidationError(
                    # "Admin and staff cannot register via token."
                # )
        # return data

    def create(self, validated_data):
        """
        Create a new voter user and associated voter profile.

        Args:
            validated_data (dict): Validated registration data

        Returns:
            User: The newly created voter user
        """
        invitation = validated_data["token"]
        password = validated_data["password"]
        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]

        user = User.objects.create_user(
            email=invitation.email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role="voter",
        )

        VoterProfile.objects.create(user=user, election_event=invitation.election_event)

        invitation.is_used = True
        invitation.save()

        return user


class AdminStaffRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for direct registration of admin and staff users.

    This serializer allows admins and staff to register directly,
    without requiring an invitation token.
    """

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password", "role"]
        extra_kwargs = {"password": {"write_only": True}, "role": {"required": True}}

    def validate_role(self, value):
        """
        Validate that only admin or staff roles can be registered directly.

        Args:
            value (str): The proposed user role

        Returns:
            str: The validated role

        Raises:
            ValidationError: If an invalid role is specified
        """
        if value not in ["admin", "staff"]:
            raise serializers.ValidationError(
                "Only admin and staff can register directly."
            )
        return value

    def create(self, validated_data):
        """
        Create a new admin or staff user.

        Args:
            validated_data (dict): Validated registration data

        Returns:
            User: The newly created admin or staff user
        """
        # Use create_user to handle password hashing
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            role=validated_data["role"],
            is_staff=validated_data["role"] == "staff",
        )
        return user
