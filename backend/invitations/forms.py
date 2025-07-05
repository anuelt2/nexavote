"""
"""
from django import forms

from invitations.models import Invitation
from election_events.models import ElectionEvent


class InvitationForm(forms.ModelForm):
    """
    """
    class Meta:
        model = Invitation
        fields = ['email', 'election_event']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['election_event'].queryset = ElectionEvent.objects.filter(is_active=True)