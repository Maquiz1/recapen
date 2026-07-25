from django import forms
from orders.models import Order
from laboratory.models import PatientTestResult

class FulfillOrderForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.order = kwargs.pop('order', None)
        super().__init__(*args, **kwargs)
        
        if self.order and self.order.test:
            self.fields['result_value'] = forms.CharField(
                label=self.order.test.test_name,
                required=True,
                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter result value...'})
            )

    def save_results(self, user):
        results = []
        val = self.cleaned_data.get('result_value')
        if val:
            res = PatientTestResult(
                patient=self.order.patient,
                test=self.order.test,
                order=self.order,
                result_value=val
            )
            if user.is_authenticated:
                res.created_by = user
                res.updated_by = user
            res.save()
            results.append(res)
        return results
