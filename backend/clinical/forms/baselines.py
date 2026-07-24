from django import forms
from clinical.models.baselines import SickleCellBaseline, DiabetesBaseline, CardiacBaseline

class SickleCellBaselineForm(forms.ModelForm):
    class Meta:
        model = SickleCellBaseline
        fields = ['visit_date', 'diagnosis_date', 'main_diagnosis', 'comments']
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'diagnosis_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'main_diagnosis': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class DiabetesBaselineForm(forms.ModelForm):
    class Meta:
        model = DiabetesBaseline
        fields = ['visit_date', 'diagnosis_date', 'main_diagnosis', 'presentation', 'hypertension', 'hypertension_date']
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'diagnosis_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'main_diagnosis': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'presentation': forms.Select(attrs={'class': 'form-select'}),
            'hypertension': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'hypertension_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class CardiacBaselineForm(forms.ModelForm):
    class Meta:
        model = CardiacBaseline
        fields = [
            'visit_date', 'diagnosis_date', 'hypertensive_heart_disease', 'coronary_artery_disease',
            'severe_uncontrolled_hypertension', 'cardiomyopathy', 'cardiomyopathy_type', 'cardiomyopathy_other',
            'rheumatic_heart_disease', 'rhd_type', 'congenital_heart_disease', 'chd_type',
            'right_heart_failure', 'right_heart_failure_type', 'pericardial_disease', 'pericardial_disease_type',
            'stroke', 'stroke_type', 'arrhythmia', 'arrhythmia_type', 'thromboembolic', 'thromboembolic_type',
            'any_other_diagnosis', 'other_diagnosis_specify', 'general_comments'
        ]
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'diagnosis_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hypertensive_heart_disease': forms.Select(attrs={'class': 'form-select'}),
            'coronary_artery_disease': forms.Select(attrs={'class': 'form-select'}),
            'severe_uncontrolled_hypertension': forms.Select(attrs={'class': 'form-select'}),
            'cardiomyopathy': forms.Select(attrs={'class': 'form-select'}),
            'cardiomyopathy_type': forms.Select(attrs={'class': 'form-select'}),
            'cardiomyopathy_other': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'rheumatic_heart_disease': forms.Select(attrs={'class': 'form-select'}),
            'rhd_type': forms.Select(attrs={'class': 'form-select'}),
            'congenital_heart_disease': forms.Select(attrs={'class': 'form-select'}),
            'chd_type': forms.Select(attrs={'class': 'form-select'}),
            'right_heart_failure': forms.Select(attrs={'class': 'form-select'}),
            'right_heart_failure_type': forms.Select(attrs={'class': 'form-select'}),
            'pericardial_disease': forms.Select(attrs={'class': 'form-select'}),
            'pericardial_disease_type': forms.Select(attrs={'class': 'form-select'}),
            'stroke': forms.Select(attrs={'class': 'form-select'}),
            'stroke_type': forms.Select(attrs={'class': 'form-select'}),
            'arrhythmia': forms.Select(attrs={'class': 'form-select'}),
            'arrhythmia_type': forms.Select(attrs={'class': 'form-select'}),
            'thromboembolic': forms.Select(attrs={'class': 'form-select'}),
            'thromboembolic_type': forms.Select(attrs={'class': 'form-select'}),
            'any_other_diagnosis': forms.Select(attrs={'class': 'form-select'}),
            'other_diagnosis_specify': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'general_comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
