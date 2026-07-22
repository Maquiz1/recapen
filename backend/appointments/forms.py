from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'scheduled_time', 'reason', 'status']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'scheduled_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'doctor': forms.Select(attrs={'class': 'form-select'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Problem', 'rows': '3'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
