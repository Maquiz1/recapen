from django import forms
from clinical.models import Vitals

class VitalsForm(forms.ModelForm):
    class Meta:
        model = Vitals
        fields = [
            'blood_pressure_systolic', 
            'blood_pressure_diastolic', 
            'heart_rate', 
            'oxygen_saturation', 
            'pain_score', 
            'notes'
        ]
        widgets = {
            'blood_pressure_systolic': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 120'}),
            'blood_pressure_diastolic': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 80'}),
            'heart_rate': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 72'}),
            'oxygen_saturation': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'e.g. 98.5'}),
            'pain_score': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 10}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
