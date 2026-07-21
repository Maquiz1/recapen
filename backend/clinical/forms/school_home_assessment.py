from django import forms
from clinical.models import SchoolHomeAssessment

class SchoolHomeAssessmentForm(forms.ModelForm):
    class Meta:
        model = SchoolHomeAssessment
        fields = [
            'visit_date', 'appropriate_grade_for_age', 'ncd_limiting_school',
            'school_days_missed', 'household_size', 'referred_from',
            'agrees_to_home_visits', 'chw_name_available', 'chw_name', 'general_comments'
        ]
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'appropriate_grade_for_age': forms.Select(attrs={'class': 'form-select'}),
            'ncd_limiting_school': forms.Select(attrs={'class': 'form-select'}),
            'school_days_missed': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 0'}),
            'household_size': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 1'}),
            'referred_from': forms.RadioSelect(choices=SchoolHomeAssessment.REFERRAL_CHOICES, attrs={'class': 'form-check-input'}),
            'agrees_to_home_visits': forms.Select(attrs={'class': 'form-select'}),
            'chw_name_available': forms.RadioSelect(choices=SchoolHomeAssessment.CHOICES_YN, attrs={'class': 'form-check-input'}),
            'chw_name': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter CHW name details...'}),
            'general_comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter general comments...'}),
        }
