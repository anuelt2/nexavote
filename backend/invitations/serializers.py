"""
"""
from rest_framework import serializers

from invitations.models import Invitation


class InvitationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for Invitation model.
    """
    class Meta:
        model = Invitation
        fields = ['email']
    
    def validate_email(self, value):
        """
        Custom validation for Invitation email field
        """
        if Invitation.objects.filter(email=value, is_used=False).exists():
            raise serializers.ValidationError("An active invitation already exists for this email")
        return value