"""
Django forms for invitation management.

This module contains form classes for creating invitations and uploading
CSV files containing voter information for bulk invitation processing.
"""
from django import forms
from django.core.exceptions import ValidationError
import csv
import io

from invitations.models import Invitation
from election_events.models import ElectionEvent


class InvitationForm(forms.ModelForm):
    """
    Form for creating individual voter invitations.
    
    Provides a Django form interface for creating voter invitations with
    validation for active election events.
    
    Meta:
        model: The Invitation model
        fields: Email and election_event fields
    """
    class Meta:
        model = Invitation
        fields = ['email', 'election_event']
    
    def __init__(self, *args, **kwargs):
        """
        Initialize the form with filtered election event choices.
        
        Limits the election_event choices to only active election events.
        
        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        super().__init__(*args, **kwargs)
        self.fields['election_event'].queryset = ElectionEvent.objects.filter(is_active=True)


class CSVUploadForm(forms.Form):
    """
    Form for uploading CSV files containing voter information.
    
    Handles file upload and validation for CSV files containing voter data
    for bulk invitation processing.
    
    Attributes:
        csv_file (FileField): File upload field for CSV files
    """
    csv_file = forms.FileField(
        label="CSV File",
        help_text="Upload a CSV file with columns: first_name, last_name, email",
        widget=forms.FileInput(attrs={'accept': '.csv'})
    )
    
    def clean_csv_file(self):
        """
        Validate the uploaded CSV file format and content.
        
        Performs comprehensive validation including file type, size, encoding,
        required columns, and data presence checks.
        
        Returns:
            File: The validated CSV file object
            
        Raises:
            ValidationError: If file format, size, encoding, or content is invalid
        """
        file = self.cleaned_data['csv_file']
        
        # Validate file extension
        if not file.name.endswith('.csv'):
            raise ValidationError("Please upload a CSV file.")
        
        # Validate file size (5MB limit)
        if file.size > 5 * 1024 * 1024:
            raise ValidationError("File size must be less than 5MB.")
        
        # Validate CSV content and structure
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
            
            # Reset file pointer for future use
            file.seek(0)
            
        except UnicodeDecodeError:
            raise ValidationError("Invalid file encoding. Please use UTF-8.")
        except csv.Error as e:
            raise ValidationError(f"Invalid CSV format: {str(e)}")
        
        return file