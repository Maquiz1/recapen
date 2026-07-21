from django import forms
from orders.models import Order
from laboratory.models import PatientTestResult

class FulfillOrderForm(forms.ModelForm):
    class Meta:
        model = PatientTestResult
        fields = ['result_value']
        widgets = {
            'result_value': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter result value...'}),
        }
