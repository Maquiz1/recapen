from django import forms
from .models import Patient, Screening, Diagnosis, Enrollment, CARDIAC_TYPE_CHOICES

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'date_of_birth', 'sex', 'phone_number', 'national_id', 'status', 'status_date', 'follow_up_interval_months', 'passport_size_photo', 'current_site']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'sex': forms.Select(attrs={'class': 'form-select'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'national_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter National ID'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'status_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'follow_up_interval_months': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'passport_size_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'current_site': forms.Select(attrs={'class': 'form-select'}),
        }

class ScreeningForm(forms.ModelForm):
    suspect_scd = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_suspect_scd'}))
    suspect_dm = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_suspect_dm'}))
    suspect_cardiac = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_suspect_cardiac'}))

    class Meta:
        model = Screening
        fields = ['date_of_screening', 'is_permanent_resident', 'known_ncd', 'type_of_screening', 'screening_notes']
        widgets = {
            'date_of_screening': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_permanent_resident': forms.Select(choices=[(True, 'Yes'), (False, 'No')], attrs={'class': 'form-select'}),
            'known_ncd': forms.Select(choices=[(True, 'Yes'), (False, 'No')], attrs={'class': 'form-select'}),
            'type_of_screening': forms.Select(attrs={'class': 'form-select'}),
            'screening_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter screening notes...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['suspect_scd'].initial = self.instance.suspected_diseases.filter(code='SCD').exists()
            self.fields['suspect_dm'].initial = self.instance.suspected_diseases.filter(code='DM').exists()
            self.fields['suspect_cardiac'].initial = self.instance.suspected_diseases.filter(code='CARDIAC').exists()

    def save(self, commit=True):
        instance = super().save(commit=commit)
        
        from diseases.models import Disease

        diseases_to_add = []
        if self.cleaned_data.get('suspect_scd'):
            diseases_to_add.append(Disease.objects.get(code='SCD'))
        if self.cleaned_data.get('suspect_dm'):
            diseases_to_add.append(Disease.objects.get(code='DM'))
        if self.cleaned_data.get('suspect_cardiac'):
            diseases_to_add.append(Disease.objects.get(code='CARDIAC'))

        if not instance.pk:
            instance.save()
        instance.suspected_diseases.set(diseases_to_add)
        return instance

class SCDInvestigationForm(forms.Form):
    lab_results = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter lab results...'}))
    radiology_results = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter radiology results...'}))
    echo_results = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter ECHO results...'}))
    scd_screening_results = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter screening results...'}))

    def __init__(self, *args, **kwargs):
        self.patient = kwargs.pop('patient', None)
        kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)
        if self.patient:
            self.fields['lab_results'].initial = self._get_val('scd_lab')
            self.fields['radiology_results'].initial = self._get_val('scd_xray')
            self.fields['echo_results'].initial = self._get_val('scd_echo')
            self.fields['scd_screening_results'].initial = self._get_val('scd_screening')

    def _get_val(self, code):
        from laboratory.models import PatientTestResult
        res = PatientTestResult.objects.filter(patient=self.patient, test__code=code).first()
        return res.result_value if res else ''

    def save(self, user=None):
        self._save_val('scd_lab', self.cleaned_data.get('lab_results'), user)
        self._save_val('scd_xray', self.cleaned_data.get('radiology_results'), user)
        self._save_val('scd_echo', self.cleaned_data.get('echo_results'), user)
        self._save_val('scd_screening', self.cleaned_data.get('scd_screening_results'), user)

    def _save_val(self, code, val, user):
        from laboratory.models import PatientTestResult
        from diagnostics.models import DiagnosticTest
        if val is not None:
            test = DiagnosticTest.objects.get(code=code)
            res, _ = PatientTestResult.objects.get_or_create(patient=self.patient, test=test)
            res.result_value = str(val)
            if user and user.is_authenticated:
                res.updated_by = user
                res.created_by = user
            res.save()

class DMInvestigationForm(forms.Form):
    hba1c = forms.DecimalField(required=False, max_digits=5, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'HbA1c (%)'}))
    c_peptide = forms.DecimalField(required=False, max_digits=5, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'C-Peptide (nmol/L)'}))
    creatinine = forms.DecimalField(required=False, max_digits=5, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Creatinine (µmol/L)'}))
    urea = forms.DecimalField(required=False, max_digits=5, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Urea (mmol/L)'}))
    rbg = forms.DecimalField(required=False, max_digits=5, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'RBG (mmol/L)'}))
    fbg = forms.DecimalField(required=False, max_digits=5, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'FBG (mmol/L)'}))

    def __init__(self, *args, **kwargs):
        self.patient = kwargs.pop('patient', None)
        kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)
        if self.patient:
            self.fields['hba1c'].initial = self._get_val('hba1c')
            self.fields['c_peptide'].initial = self._get_val('c_peptide')
            self.fields['creatinine'].initial = self._get_val('creatinine')
            self.fields['urea'].initial = self._get_val('urea')
            self.fields['rbg'].initial = self._get_val('rbg')
            self.fields['fbg'].initial = self._get_val('fbg')

    def _get_val(self, code):
        from laboratory.models import PatientTestResult
        res = PatientTestResult.objects.filter(patient=self.patient, test__code=code).first()
        return float(res.result_value) if res and res.result_value else None

    def save(self, user=None):
        self._save_val('hba1c', self.cleaned_data.get('hba1c'), user)
        self._save_val('c_peptide', self.cleaned_data.get('c_peptide'), user)
        self._save_val('creatinine', self.cleaned_data.get('creatinine'), user)
        self._save_val('urea', self.cleaned_data.get('urea'), user)
        self._save_val('rbg', self.cleaned_data.get('rbg'), user)
        self._save_val('fbg', self.cleaned_data.get('fbg'), user)

    def _save_val(self, code, val, user):
        from laboratory.models import PatientTestResult
        from diagnostics.models import DiagnosticTest
        if val is not None:
            test = DiagnosticTest.objects.get(code=code)
            res, _ = PatientTestResult.objects.get_or_create(patient=self.patient, test=test)
            res.result_value = str(val)
            if user and user.is_authenticated:
                res.updated_by = user
                res.created_by = user
            res.save()

class CardiacInvestigationForm(forms.Form):
    cardiac_type = forms.ChoiceField(choices=[('', '--- Select Cardiac Type ---')] + list(CARDIAC_TYPE_CHOICES), required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    lab_results = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter lab results...'}))
    echo_results = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter ECHO results...'}))
    ecg_results = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter ECG details...'}))
    xray_results = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter chest X-Ray notes...'}))

    def __init__(self, *args, **kwargs):
        self.patient = kwargs.pop('patient', None)
        kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)
        if self.patient:
            self.fields['cardiac_type'].initial = self._get_val('cardiac_type')
            self.fields['lab_results'].initial = self._get_val('cardiac_lab')
            self.fields['echo_results'].initial = self._get_val('cardiac_echo')
            self.fields['ecg_results'].initial = self._get_val('ecg')
            self.fields['xray_results'].initial = self._get_val('cardiac_xray')

    def _get_val(self, code):
        from laboratory.models import PatientTestResult
        res = PatientTestResult.objects.filter(patient=self.patient, test__code=code).first()
        return res.result_value if res else ''

    def save(self, user=None):
        self._save_val('cardiac_type', self.cleaned_data.get('cardiac_type'), user)
        self._save_val('cardiac_lab', self.cleaned_data.get('lab_results'), user)
        self._save_val('cardiac_echo', self.cleaned_data.get('echo_results'), user)
        self._save_val('ecg', self.cleaned_data.get('ecg_results'), user)
        self._save_val('cardiac_xray', self.cleaned_data.get('xray_results'), user)

    def _save_val(self, code, val, user):
        from laboratory.models import PatientTestResult
        from diagnostics.models import DiagnosticTest
        if val is not None and val != '':
            test, _ = DiagnosticTest.objects.get_or_create(code=code, defaults={'test_name': code.replace('_', ' ').title(), })
            res, _ = PatientTestResult.objects.get_or_create(patient=self.patient, test=test)
            res.result_value = str(val)
            if user and user.is_authenticated:
                res.updated_by = user
                res.created_by = user
            res.save()

class DiagnosisForm(forms.ModelForm):
    confirmed_scd = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_confirmed_scd'}))
    confirmed_dm = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_confirmed_dm'}))
    confirmed_cardiac = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_confirmed_cardiac'}))

    class Meta:
        model = Diagnosis
        fields = ['consent_given', 'date_of_consent', 'diagnosis', 'confirmed_cardiac_type', 'comments']
        widgets = {
            'consent_given': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_consent_given'}),
            'date_of_consent': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Diagnosis...', 'required': 'required'}),
            'confirmed_cardiac_type': forms.Select(attrs={'class': 'form-select', 'id': 'id_confirmed_cardiac_type'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Clinical comments...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['confirmed_scd'].initial = self.instance.confirmed_diseases.filter(code='SCD').exists()
            self.fields['confirmed_dm'].initial = self.instance.confirmed_diseases.filter(code='DM').exists()
            self.fields['confirmed_cardiac'].initial = self.instance.confirmed_diseases.filter(code='CARDIAC').exists()

    def save(self, commit=True):
        instance = super().save(commit=commit)
        
        from diseases.models import Disease
        diseases_to_add = []
        if self.cleaned_data.get('confirmed_scd'):
            diseases_to_add.append(Disease.objects.get(code='SCD'))
        if self.cleaned_data.get('confirmed_dm'):
            diseases_to_add.append(Disease.objects.get(code='DM'))
        if self.cleaned_data.get('confirmed_cardiac'):
            diseases_to_add.append(Disease.objects.get(code='CARDIAC'))
            
        if not instance.pk:
            instance.save()
        instance.confirmed_diseases.set(diseases_to_add)
        return instance

    def clean(self):
        cleaned_data = super().clean()
        confirmed_cardiac = cleaned_data.get('confirmed_cardiac')
        confirmed_cardiac_type = cleaned_data.get('confirmed_cardiac_type')
        
        if confirmed_cardiac and not confirmed_cardiac_type:
            self.add_error('confirmed_cardiac_type', 'Please select a cardiac condition type.')
        return cleaned_data

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['is_eligible', 'cohort', 'remarks']
        widgets = {
            'is_eligible': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'is_eligible_checkbox'}),
            'cohort': forms.Select(attrs={'class': 'form-select'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Explanation if not eligible', 'id': 'remarks_input'}),
        }

class TestRequestsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.patient = kwargs.pop('patient', None)
        super().__init__(*args, **kwargs)
        from diagnostics.models import DiagnosticTest
        from django.db.models import Q
        tests = DiagnosticTest.objects.filter(
            is_active=True
        ).exclude(
            Q(diagnostic_group__is_active=False) | Q(diagnostic_category__is_active=False)
        ).select_related('diagnostic_group', 'diagnostic_category', 'department').order_by('department__name', 'diagnostic_group__name', 'diagnostic_category__name', 'test_name')
        
        self.grouped_fields = {}
        for test in tests:
            field_name = f'test_{test.id}'
            self.fields[field_name] = forms.BooleanField(
                required=False, 
                label=test.test_name,
                widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
            )
            dept = test.department.name if test.department else 'General'
            if dept not in self.grouped_fields:
                self.grouped_fields[dept] = {}
                
            group_name = test.diagnostic_group.name if test.diagnostic_group else "Other"
            cat_name = test.diagnostic_category.name if test.diagnostic_category else "General"
            
            if group_name not in self.grouped_fields[dept]:
                self.grouped_fields[dept][group_name] = {}
            if cat_name not in self.grouped_fields[dept][group_name]:
                self.grouped_fields[dept][group_name][cat_name] = []
            self.grouped_fields[dept][group_name][cat_name].append(self[field_name])

    def save(self, user=None):
        from orders.models import Order
        from encounters.models import Encounter
        from diagnostics.models import DiagnosticTest
        orders_created = []
        encounter = Encounter.objects.filter(patient=self.patient, status='in_progress').first()
        if not encounter:
            encounter = Encounter.objects.create(patient=self.patient, status='in_progress', doctor=user if user.is_authenticated else None)

        for field_name, value in self.cleaned_data.items():
            if field_name.startswith('test_') and value:
                test_id = field_name.split('_')[1]
                test = DiagnosticTest.objects.get(id=test_id)
                
                order_type = test.department.name.lower() if test.department else 'other'

                order = Order.objects.create(
                    patient=self.patient,
                    encounter=encounter,
                    test=test,
                    order_type=order_type,
                    ordering_doctor=user if user and user.is_authenticated else None,
                    status='pending'
                )
                orders_created.append(order)
        return orders_created
