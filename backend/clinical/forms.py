from django import forms
from .models import SCDVitals

class SCDVitalsForm(forms.ModelForm):
    class Meta:
        model = SCDVitals
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
            'heart_rate': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'BPM'}),
            'oxygen_saturation': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '%', 'step': '0.1'}),
            'pain_score': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 10, 'placeholder': '0-10'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
