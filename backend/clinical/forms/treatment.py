from django import forms
from clinical.models import Treatment

class TreatmentForm(forms.ModelForm):
    class Meta:
        model = Treatment
        fields = [
            'vaccination_needed', 'vaccination_which',
            'transfusion_needed', 'transfusion_units',
            'education_diet', 'education_hydration', 'education_acute_symptoms', 
            'education_fever', 'education_lifestyle', 'education_misconception',
            'social_support_provided', 'social_support_type',
            'other_support_provided', 'other_support_specify',
            'referrals_provided', 'referrals_type',
            'notes'
        ]
        widgets = {
            'vaccination_needed': forms.RadioSelect(choices=Treatment.CHOICES_YN, attrs={'class': 'form-check-input'}),
            'vaccination_which': forms.TextInput(attrs={'class': 'form-control'}),
            'transfusion_needed': forms.RadioSelect(choices=Treatment.CHOICES_YN, attrs={'class': 'form-check-input'}),
            'transfusion_units': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            
            'education_diet': forms.Select(attrs={'class': 'form-select'}),
            'education_hydration': forms.Select(attrs={'class': 'form-select'}),
            'education_acute_symptoms': forms.Select(attrs={'class': 'form-select'}),
            'education_fever': forms.Select(attrs={'class': 'form-select'}),
            'education_lifestyle': forms.Select(attrs={'class': 'form-select'}),
            'education_misconception': forms.Select(attrs={'class': 'form-select'}),
            
            'social_support_provided': forms.RadioSelect(choices=Treatment.CHOICES_YN, attrs={'class': 'form-check-input'}),
            'social_support_type': forms.TextInput(attrs={'class': 'form-control'}),
            'other_support_provided': forms.RadioSelect(choices=Treatment.CHOICES_YN, attrs={'class': 'form-check-input'}),
            'other_support_specify': forms.TextInput(attrs={'class': 'form-control'}),
            'referrals_provided': forms.RadioSelect(choices=Treatment.CHOICES_YN, attrs={'class': 'form-check-input'}),
            'referrals_type': forms.TextInput(attrs={'class': 'form-control'}),
            
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
