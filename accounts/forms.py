# accounts/forms.py
from .models import Account
from django.core.exceptions import ValidationError
from accounts.models import Account
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'password1', 'password2')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone',
                  'email', 'description', 'category', 'picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel', 'placeholder': '(XX) XXXXX-XXXX'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'picture': forms.FileInput(attrs={'class': 'form-control-file', 'accept': 'image/*'}),
        }

        help_texts = {
            'first_name': 'Enter your first name.',
            'last_name': 'Enter your last name.',
            'phone': 'Enter your phone number, including area code.',
            'email': 'Enter a valid email address.',
            'description': 'Provide a brief description.',
            'category': 'Select the appropriate category.',
        }

    def __init__(self, *args, **kwargs):
        # Remove the 'disabled' parameter from kwargs if it exists
        disable_fields = kwargs.pop('disable_fields', False)
        super(AccountForm, self).__init__(*args, **kwargs)
        if disable_fields:
            # Disable all fields if disable_fields is True
            for field in self.fields.values():
                field.widget.attrs['disabled'] = 'true'

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name and len(first_name) < 3:
            raise ValidationError(
                'First name must be at least 3 characters long.')
        return first_name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.isdigit():
            raise ValidationError('Phone number must contain only digits.')
        if phone and (len(phone) < 10 or len(phone) > 15):
            raise ValidationError(
                'Phone number must be between 10 and 15 digits.')
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and "@example.com" in email:
            raise ValidationError(
                'Registration using "@example.com" emails is not allowed.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if first_name and last_name and first_name == last_name:
            raise ValidationError(
                'First name and last name cannot be the same.')

        return cleaned_data
