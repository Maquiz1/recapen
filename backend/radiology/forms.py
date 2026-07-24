from django import forms
from laboratory.models import LaboratoryTest

class RadiologyTestForm(forms.ModelForm):
    class Meta:
        model = LaboratoryTest
        fields = ['name', 'code', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter imaging test name'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter unique code (e.g. chest_xray)'}),
            
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter test description...'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
