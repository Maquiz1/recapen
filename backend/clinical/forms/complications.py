from django import forms
from clinical.models import Complications

class ComplicationsForm(forms.ModelForm):
    class Meta:
        model = Complications
        fields = [
            'stroke', 'kidney_disease', 'retinopathy', 'neuropathy',
            'diabetic_foot', 'cardiovascular_disease', 'other_complications'
        ]
        widgets = {
            'stroke': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'kidney_disease': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'retinopathy': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'neuropathy': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'diabetic_foot': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cardiovascular_disease': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'other_complications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe other complications...'}),
        }
