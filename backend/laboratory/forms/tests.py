from django import forms
from diagnostics.models import DiagnosticTest

class LabTestForm(forms.ModelForm):
    class Meta:
        model = DiagnosticTest
        fields = ['test_name', 'code', 'diagnostic_group', 'diagnostic_category', 'range_min', 'range_max', 'units', 'cost', 'description', 'is_active']
        widgets = {
            'test_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter unique code (e.g. hba1c)'}),
            'diagnostic_group': forms.Select(attrs={'class': 'form-select'}),
            'diagnostic_category': forms.Select(attrs={'class': 'form-select'}),
            'range_min': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 0'}),
            'range_max': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 10'}),
            'units': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. g/dl'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter description...'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'diagnostic_group': 'Diagnostic Group',
            'diagnostic_category': 'Diagnostic Category',
            'test_name': 'Test Name'
        }
