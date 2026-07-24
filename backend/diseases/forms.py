from django import forms
from .models import Disease

class DiseaseForm(forms.ModelForm):
    class Meta:
        model = Disease
        fields = ['name', 'code', 'description', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Disease Name'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. DM, SCD'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description...'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }
