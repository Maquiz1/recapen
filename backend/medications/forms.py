from django import forms
from .models import Medication

class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['name', 'generic_name', 'form', 'strength', 'description', 'is_active']
        
class InventoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['stock_quantity']
        widgets = {
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }


