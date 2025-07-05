"""
"""
from django import forms

from elections.models import Candidate, Election
from election_events.models import ElectionEvent


class CandidateForm(forms.ModelForm):
    """
    """
    class Meta:
        model = Candidate
        fields = ['election', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        """
        """
        super().__init__(*args, **kwargs)
        self.fields['election'].queryset = Election.objects.all()


class ElectionForm(forms.ModelForm):
    """
    """
    class Meta:
        model = Election
        fields = ['election_event', 'title', 'description']
    
    def __init__(self, *args, **kwargs):
        """
        """
        super().__init__(*args, **kwargs)
        self.fields['election_event'].queryset = ElectionEvent.objects.filter(is_active=True)