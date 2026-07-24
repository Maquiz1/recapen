from django import forms
from diagnostics.models import DiagnosticGroup, DiagnosticCategory

class CategoryForm(forms.ModelForm):
    class Meta:
        model = DiagnosticGroup
        fields = ['name', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Haematology'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter description...'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class TypeForm(forms.ModelForm):
    class Meta:
        model = DiagnosticCategory
        fields = ['group', 'name', 'description', 'is_active']
        widgets = {
            'group': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Renal Function Test'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter description...'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
