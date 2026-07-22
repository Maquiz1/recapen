from django import forms
from ..models import Prescription

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['medication', 'start_date', 'end_date', 'action', 'dose_description', 'dose_duration']
        widgets = {
            'medication': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'action': forms.Select(attrs={'class': 'form-select'}),
            'dose_description': forms.TextInput(attrs={'class': 'form-control'}),
            'dose_duration': forms.TextInput(attrs={'class': 'form-control'}),
        }
