from django import forms
from .models import PatientDocument

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = PatientDocument
        fields = ['document_type', 'file', 'description']
        widgets = {
            'document_type': forms.Select(attrs={'class': 'form-select'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional brief description...'}),
        }
