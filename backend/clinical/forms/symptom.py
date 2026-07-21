from django import forms
from clinical.models import Symptom

class SymptomForm(forms.ModelForm):
    class Meta:
        model = Symptom
        fields = ['reported_symptoms', 'severity', 'duration_days']
        widgets = {
            'reported_symptoms': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'List reported symptoms...'}),
            'severity': forms.Select(attrs={'class': 'form-select'}),
            'duration_days': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duration in days'}),
        }
