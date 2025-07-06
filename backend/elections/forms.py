"""
elections/forms.py

This module defines Django forms for the elections application.
Contains forms for creating and editing candidates and elections.
"""
from django import forms

from elections.models import Candidate, Election
from election_events.models import ElectionEvent


class CandidateForm(forms.ModelForm):
    """
    Django form for creating and editing Candidate objects.
    
    This form provides a user interface for creating new candidates
    and editing existing ones, with validation and field customization.
    
    Meta:
        model: The Candidate model class
        fields: List of fields to include in the form
    """
    class Meta:
        model = Candidate
        fields = ['election', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with custom field configurations.
        
        Customizes the election field queryset to show all available elections.
        
        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        super().__init__(*args, **kwargs)
        self.fields['election'].queryset = Election.objects.all()


class ElectionForm(forms.ModelForm):
    """
    Django form for creating and editing Election objects.
    
    This form provides a user interface for creating new elections
    and editing existing ones, with validation and field customization.
    
    Meta:
        model: The Election model class
        fields: List of fields to include in the form
    """
    class Meta:
        model = Election
        fields = ['election_event', 'title', 'description']
    
    def __init__(self, *args, **kwargs):
        """
        Initialize the form with custom field configurations.
        
        Customizes the election_event field queryset to show only active
        election events.
        
        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        super().__init__(*args, **kwargs)
        self.fields['election_event'].queryset = ElectionEvent.objects.filter(is_active=True)
