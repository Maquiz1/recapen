from django import forms
from clinical.models import Hospitalization

class HospitalizationForm(forms.ModelForm):
    class Meta:
        model = Hospitalization
        fields = [
            'recent_hospitalizations',
            'num_hospitalizations_12m',
            'for_ncd',
            'num_hospitalizations_ncd_12m',
            'school_days_missed_last_month',
            'transfusions_past_month',
            'taking_malaria_prophylaxis',
            'taking_insecticide_net',
            'taking_folic_acid',
            'taking_penicillin_prophylaxis',
            'pneumococcal_vaccination_up_to_date',
            'on_chronic_opioid_therapy',
            'on_hydroxyurea',
            'hydroxyurea_start_date',
            'hydroxyurea_dose',
        ]
        widgets = {
            'recent_hospitalizations': forms.RadioSelect(choices=Hospitalization.CHOICES_YN, attrs={'class': 'form-check-input'}),
            'num_hospitalizations_12m': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 0'}),
            'for_ncd': forms.RadioSelect(choices=[('yes', 'Yes'), ('no', 'No'), ('unset', 'Unset')], attrs={'class': 'form-check-input'}),
            'num_hospitalizations_ncd_12m': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 0'}),
            
            'school_days_missed_last_month': forms.NumberInput(attrs={'class': 'form-control'}),
            'transfusions_past_month': forms.NumberInput(attrs={'class': 'form-control'}),
            
            'taking_malaria_prophylaxis': forms.Select(attrs={'class': 'form-select'}),
            'taking_insecticide_net': forms.Select(attrs={'class': 'form-select'}),
            'taking_folic_acid': forms.Select(attrs={'class': 'form-select'}),
            'taking_penicillin_prophylaxis': forms.Select(attrs={'class': 'form-select'}),
            'pneumococcal_vaccination_up_to_date': forms.Select(attrs={'class': 'form-select'}),
            
            'on_chronic_opioid_therapy': forms.RadioSelect(choices=Hospitalization.CHOICES_YN_NA, attrs={'class': 'form-check-input'}),
            'on_hydroxyurea': forms.RadioSelect(choices=Hospitalization.CHOICES_YN_NA, attrs={'class': 'form-check-input'}),
            'hydroxyurea_start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hydroxyurea_dose': forms.NumberInput(attrs={'class': 'form-control'}),
        }
