"""
"""
from django import forms
from election_events.models import ElectionEvent


class ElectionEventForm(forms.ModelForm):
    """
    """
    class Meta:
        model = ElectionEvent
        fields = ['title', 'description', 'start_time', 'end_time']
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
        """
        super().__init__(*args, **kwargs)
        self.fields['start_time'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['end_time'].input_formats = ['%Y-%m-%dT%H:%M']