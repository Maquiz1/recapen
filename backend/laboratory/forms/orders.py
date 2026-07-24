from django import forms
from orders.models import Order
from laboratory.models import PatientTestResult

class FulfillOrderForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.order = kwargs.pop('order', None)
        super().__init__(*args, **kwargs)
        
        if self.order and self.order.test:
            if self.order.test.is_panel:
                # Add a field for each sub-test
                for sub in self.order.test.sub_tests.all():
                    self.fields[f'test_{sub.pk}'] = forms.CharField(
                        label=sub.name,
                        required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': f'Enter {sub.name}...'})
                    )
            else:
                self.fields['result_value'] = forms.CharField(
                    label=self.order.test.name,
                    required=True,
                    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter result value...'})
                )

    def save_results(self, user):
        results = []
        if self.order.test.is_panel:
            for sub in self.order.test.sub_tests.all():
                val = self.cleaned_data.get(f'test_{sub.pk}')
                if val:
                    res = PatientTestResult(
                        patient=self.order.patient,
                        test=sub,
                        order=self.order,
                        result_value=val
                    )
                    if user.is_authenticated:
                        res.created_by = user
                        res.updated_by = user
                    res.save()
                    results.append(res)
        else:
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
