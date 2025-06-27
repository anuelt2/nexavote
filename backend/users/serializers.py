"""
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model

from invitations.models import Invitation
from users.models import User, VoterProfile

User = get_user_model()


class RegisterViaTokenSerializer(serializers.Serializer):
    """
    """
    invitation = serializers.UUIDField()
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
            raise serializers.ValidationError('Invalid or expired token.')
        return invitation

    def create(self, validated_data):
        """
        """
        invitation = validated_data['invitation']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']

        user = User.objects.create_user(
                email=invitation.email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role='voter'
                )

        VoterProfile.objects.create(
            user=user,
            election_event=invitation.election_event
        )

        invitation.is_used = True
        invitation.save()

        return user
