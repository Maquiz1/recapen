from django import forms
from .models import Vitals, Hospitalization, Risk, Socioeconomic, Treatment

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

class HospitalizationForm(forms.ModelForm):
    class Meta:
        model = Hospitalization
        fields = [
            'admission_date',
            'discharge_date',
            'reason_for_admission',
            'ward',
            'outcome',
            'discharge_summary'
        ]
        widgets = {
            'admission_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'discharge_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reason_for_admission': forms.TextInput(attrs={'class': 'form-control'}),
            'ward': forms.TextInput(attrs={'class': 'form-control'}),
            'outcome': forms.Select(attrs={'class': 'form-select'}),
            'discharge_summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class RiskForm(forms.ModelForm):
    class Meta:
        model = Risk
        fields = ['smoking_status', 'alcohol_use', 'physical_inactivity', 'family_history_ncd', 'unhealthy_diet']
        widgets = {
            'smoking_status': forms.Select(attrs={'class': 'form-select'}),
            'alcohol_use': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'physical_inactivity': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'family_history_ncd': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'unhealthy_diet': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class SocioeconomicForm(forms.ModelForm):
    class Meta:
        model = Socioeconomic
        fields = ['education_level', 'employment_status', 'monthly_income', 'access_clean_water', 'has_health_insurance']
        widgets = {
            'education_level': forms.Select(attrs={'class': 'form-select'}),
            'employment_status': forms.Select(attrs={'class': 'form-select'}),
            'monthly_income': forms.TextInput(attrs={'class': 'form-control'}),
            'access_clean_water': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_health_insurance': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

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
