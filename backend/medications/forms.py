from django import forms
from .models import Medication

class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['name', 'generic_name', 'form', 'strength', 'strength_unit', 'description', 'reorder_level', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Tylenol'}),
            'generic_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Paracetamol'}),
            'form': forms.Select(attrs={'class': 'form-select'}),
            'strength': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 500'}),
            'strength_unit': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'reorder_level': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
class InventoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['stock_quantity']
        widgets = {
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }


