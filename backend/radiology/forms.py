from django import forms
from laboratory.models import LabTest

class RadiologyTestForm(forms.ModelForm):
    class Meta:
        model = LabTest
        fields = ['name', 'code', 'diseases', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter imaging test name'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter unique code (e.g. chest_xray)'}),
            'diseases': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 5}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter test description...'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.category = 'radiology'
        if commit:
            instance.save()
            self.save_m2m()
        return instance
