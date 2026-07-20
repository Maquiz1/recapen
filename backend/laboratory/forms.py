from django import forms
from .models import LabTest

class LabTestForm(forms.ModelForm):
    class Meta:
        model = LabTest
        fields = ['name', 'code', 'category', 'diseases', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter test name'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter unique code (e.g. hba1c)'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'diseases': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 5}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter test description...'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
