from django import forms
from laboratory.models import LaboratoryTest

class LabTestForm(forms.ModelForm):
    class Meta:
        model = LaboratoryTest
        fields = ['name', 'code', 'laboratory_category', 'laboratory_type', 'range_min', 'range_max', 'units', 'cost', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter unique code (e.g. hba1c)'}),
            'laboratory_category': forms.Select(attrs={'class': 'form-select'}),
            'laboratory_type': forms.Select(attrs={'class': 'form-select'}),
            'range_min': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'range_max': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'units': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. g/dl'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter description...'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'laboratory_category': 'Laboratory Category',
            'laboratory_type': 'Laboratory Type',
        }
