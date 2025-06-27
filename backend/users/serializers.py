"""
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model

from invitations.models import Invitation
from users.models import VoterProfile

User = get_user_model()


class RegisterViaTokenSerializer(serializers.Serializer):
    """
    """
    token = serializers.UUIDField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate_token(self, value):
        """
        """
        try:
            invitation = Invitation.objects.get(token=value, is_used=False)
        except Invitation.DoesNotExist:
            raise serializers.ValidationError('Invalid or expired token.')
        return invitation

    def create(self, validated_data):
        """
        """
        invitation = validated_data['token']
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

        VoterProfile.objects.create(user=user)

        invitation.is_used = True
        invitation.save()

        return user
