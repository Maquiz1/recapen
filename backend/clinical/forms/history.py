from django import forms
from clinical.models import History

class HistoryForm(forms.ModelForm):
    class Meta:
        model = History
        fields = ['medical_history', 'family_history', 'surgical_history']
        widgets = {
            'medical_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter past medical history...'}),
            'family_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter family medical history...'}),
            'surgical_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter past surgical history...'}),
        }
