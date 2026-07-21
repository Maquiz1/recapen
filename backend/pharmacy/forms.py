from django import forms
from .models import Dispensation

class DispensationForm(forms.ModelForm):
    class Meta:
        model = Dispensation
        fields = ['quantity_dispensed', 'notes']
        widgets = {
            'quantity_dispensed': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Optional dispensing notes or counseling provided...'}),
        }
