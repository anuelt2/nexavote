"""
Django forms for user registration and authentication.

This module contains form classes for handling voter registration
with password validation and confirmation.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class VoterRegistrationForm(forms.Form):
    """
    Form for voter registration with password confirmation.
    
    Handles voter registration with first name, last name, email,
    and password confirmation fields.
    """
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    email = forms.EmailField(disabled=True)
    
    def clean(self):
        """
        Validate that passwords match.
        
        Returns:
            dict: Cleaned form data
            
        Raises:
            ValidationError: If passwords don't match
        """
        cleaned_data = super().clean()
        pwd1 = cleaned_data.get("password1")
        pwd2 = cleaned_data.get("password2")
        
        if pwd1 and pwd2 and pwd1 != pwd2:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data
