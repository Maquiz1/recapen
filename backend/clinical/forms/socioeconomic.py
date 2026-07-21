from django import forms
from clinical.models import Socioeconomic

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
