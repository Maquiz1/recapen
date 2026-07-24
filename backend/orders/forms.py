from django import forms
from .models import Order
from medications.models import Medication
from diagnostics.models import DiagnosticTest

class OrderLabTestForm(forms.ModelForm):
    test = forms.ModelChoiceField(
        queryset=DiagnosticTest.objects.filter(is_active=True, department__name='laboratory'),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Select Laboratory Test..."
    )
    
    class Meta:
        model = Order
        fields = ['test', 'urgency', 'clinical_notes']
        widgets = {
            'urgency': forms.Select(attrs={'class': 'form-select'}),
            'clinical_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Reason for ordering test...'}),
        }

class PrescriptionForm(forms.ModelForm):
    medication = forms.ModelChoiceField(
        queryset=Medication.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Select Medication..."
    )
    
    class Meta:
        model = Order
        fields = ['medication', 'dosage_instructions', 'urgency', 'clinical_notes']
        widgets = {
            'dosage_instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'e.g. 1 tablet by mouth twice daily for 7 days'}),
            'urgency': forms.Select(attrs={'class': 'form-select'}),
            'clinical_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Reason for prescribing...'}),
        }
