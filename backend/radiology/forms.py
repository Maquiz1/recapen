from django import forms
from diagnostics.models import DiagnosticTest

class RadiologyTestForm(forms.ModelForm):
    class Meta:
        model = DiagnosticTest
        fields = ['test_name', 'code', 'diagnostic_group', 'diagnostic_category', 'cost', 'description', 'is_active']
        widgets = {
            'test_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter imaging test name'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter unique code (e.g. chest_xray)'}),
            'diagnostic_group': forms.Select(attrs={'class': 'form-select'}),
            'diagnostic_category': forms.Select(attrs={'class': 'form-select'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter test description...'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'diagnostic_group': 'Diagnostic Group',
            'diagnostic_category': 'Diagnostic Category',
            'test_name': 'Test Name'
        }
