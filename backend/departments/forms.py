from django import forms
from .models import Department

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'email', 'head', 'phone_number', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Department Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}),
            'head': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Department Head'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            # For is_active, we use RadioSelect to match the template's active/inactive radios
            'is_active': forms.RadioSelect(choices=[(True, 'Active'), (False, 'Inactive')], attrs={'class': 'form-check-input'})
        }
