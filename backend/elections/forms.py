"""
"""
from django import forms

from elections.models import Candidate, Election
from election_events.models import ElectionEvent


class ElectionForm(forms.ModelForm):
    """
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
    """
    class Meta:
        model = Candidate
        fields = ['first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        """
        """
        super().__init__(*args, **kwargs)
        # self.fields['election'].queryset = Election.objects.all()