from django import forms
from clinical.models import Risk

class RiskForm(forms.ModelForm):
    class Meta:
        model = Risk
        fields = [
            'tobacco', 'alcohol', 'employment_status', 'ncd_limiting_school',
            'hiv_status', 'tb_status', 'tb_screening_date'
        ]
        widgets = {
            'tobacco': forms.Select(attrs={'class': 'form-select'}),
            'alcohol': forms.Select(attrs={'class': 'form-select'}),
            'employment_status': forms.Select(attrs={'class': 'form-select'}),
            'ncd_limiting_school': forms.Select(attrs={'class': 'form-select'}),
            'hiv_status': forms.RadioSelect(choices=Risk.HIV_CHOICES, attrs={'class': 'form-check-input'}),
            'tb_status': forms.RadioSelect(choices=Risk.TB_CHOICES, attrs={'class': 'form-check-input'}),
            'tb_screening_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
