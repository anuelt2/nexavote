"""
elections/forms.py

This module defines Django forms for the elections application.
Contains forms for creating and editing candidates and elections.
"""
from django import forms

from elections.models import Candidate, Election
from election_events.models import ElectionEvent


class ElectionForm(forms.ModelForm):
    """
    Django form for creating and editing Candidate objects.
    
    This form provides a user interface for creating new candidates
    and editing existing ones, with validation and field customization.
    
    Meta:
        model: The Candidate model class
        fields: List of fields to include in the form
    """
    start_time = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            format='%Y-%m-%dT%H:%M',
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local',
                    'placeholder': 'DD/MM/YYYY HH:MM',
                }
        )
    )
    end_time = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            format='%Y-%m-%dT%H:%M',
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local',
                    'placeholder': 'DD/MM/YYYY HH:MM',
                }
        )
    )

    class Meta:
        model = Election
        fields = ['election_event', 'title', 'description', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local',
                    'placeholder': 'DD/MM/YYYY HH:MM'
                }
            ),
            'end_time': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local',
                    'placeholder': 'DD/MM/YYYY HH:MM'
                }
            ),
        }
    
    def __init__(self, *args, **kwargs):
        """
        Initialize the form with custom field configurations.
        
        Customizes the election field queryset to show all available elections.
        
        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        super().__init__(*args, **kwargs)
        self.fields['election_event'].queryset = ElectionEvent.objects.filter(is_active=True)
        self.fields['start_time'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['end_time'].input_formats = ['%Y-%m-%dT%H:%M']

        event = self.initial.get('election_event')
        if event and isinstance(event, ElectionEvent):
            self.initial.setdefault('start_time', event.start_time.strftime('%Y-%m-%dT%H:%M'))
            self.initial.setdefault('end_time', event.end_time.strftime('%Y-%m-%dT%H:%M'))
    
    def clean(self):
        """
        """
        cleaned_data = super().clean()
        start = cleaned_data.get('start_time')
        end = cleaned_data.get('end_time')
        event = cleaned_data.get('election_event')

        if not start and event:
            cleaned_data['start_time'] = event.start_time
        if not end and event:
            cleaned_data['end_time'] = event.end_time
        
        return cleaned_data


class CandidateForm(forms.ModelForm):
    """
    Django form for creating and editing Election objects.
    
    This form provides a user interface for creating new elections
    and editing existing ones, with validation and field customization.
    
    Meta:
        model: The Election model class
        fields: List of fields to include in the form
    """
    class Meta:
        model = Candidate
        fields = ['first_name', 'last_name']

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
        # self.fields['election'].queryset = Election.objects.all()