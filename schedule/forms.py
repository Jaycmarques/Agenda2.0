from django import forms
from accounts.models import Account
from django_select2.forms import Select2MultipleWidget 
from .models import Meeting


class MeetingForm(forms.ModelForm):
    invited_contacts = forms.ModelMultipleChoiceField(
        queryset=Account.objects.all(),
        widget=Select2MultipleWidget,  # Dropdown com busca
        required=False,
        label="Invite Contacts"
    )

    class Meta:
        model = Meeting
        fields = ['title', 'start_time', 'end_time', 'invited_contacts']


    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and start_time > end_time:
            self.add_error('start_time', "Start date and time cannot be later than the end date and time.")
            self.add_error('end_time', "Ensure the end date and time is after the start time.")
        
        return cleaned_data