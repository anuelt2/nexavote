"""
"""
from django import forms

from invitations.models import Invitation
from election_events.models import ElectionEvent
from django import forms
from django.core.exceptions import ValidationError
import csv
import io


class InvitationForm(forms.ModelForm):
    """
    """
    class Meta:
        model = Invitation
        fields = ['email', 'election_event']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['election_event'].queryset = ElectionEvent.objects.filter(is_active=True)



class CSVUploadForm(forms.Form):
    """
    Form for uploading CSV files containing voter information.
    """
    csv_file = forms.FileField(
        label="CSV File",
        help_text="Upload a CSV file with columns: first_name, last_name, email",
        widget=forms.FileInput(attrs={'accept': '.csv'})
    )
    
    def clean_csv_file(self):
        """
        Validate the uploaded CSV file.
        """
        file = self.cleaned_data['csv_file']
        
        if not file.name.endswith('.csv'):
            raise ValidationError("Please upload a CSV file.")
        
        if file.size > 5 * 1024 * 1024:  # 5MB limit
            raise ValidationError("File size must be less than 5MB.")
        
        # Read and validate CSV content
        try:
            file.seek(0)
            content = file.read().decode('utf-8')
            csv_reader = csv.DictReader(io.StringIO(content))
            
            # Check for required columns
            required_columns = {'first_name', 'last_name', 'email'}
            if not required_columns.issubset(set(csv_reader.fieldnames)):
                raise ValidationError(
                    f"CSV must contain columns: {', '.join(required_columns)}"
                )
            
            # Validate at least one row exists
            rows = list(csv_reader)
            if not rows:
                raise ValidationError("CSV file is empty.")
            
            # Reset file pointer
            file.seek(0)
            
        except UnicodeDecodeError:
            raise ValidationError("Invalid file encoding. Please use UTF-8.")
        except csv.Error as e:
            raise ValidationError(f"Invalid CSV format: {str(e)}")
        
        return file