from django import forms
from .models import Patient, Screening, Consultation, Enrollment, CARDIAC_TYPE_CHOICES

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'phone_number', 'national_id']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'national_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter National ID'}),
        }

class ScreeningForm(forms.ModelForm):
    suspect_scd = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_suspect_scd'}))
    suspect_dm = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_suspect_dm'}))
    suspect_cardiac = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_suspect_cardiac'}))

    # We also render test checkbox choices dynamically. But since the HTML has specific static fields,
    # we bind the dynamic checked tests in save() and load them in __init__ for backward compatibility.
    order_scd_lab = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input scd-test'}))
    order_scd_radiology = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input scd-test'}))
    order_scd_echo = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input scd-test'}))
    order_scd_screening = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input scd-test'}))

    order_dm_hba1c = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input dm-test'}))
    order_dm_c_peptide = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input dm-test'}))
    order_dm_creatinine = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input dm-test'}))
    order_dm_urea = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input dm-test'}))
    order_dm_rbg = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input dm-test'}))
    order_dm_fbg = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input dm-test'}))

    order_cardiac_lab = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input cardiac-test'}))
    order_cardiac_echo = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input cardiac-test'}))
    order_cardiac_ecg = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input cardiac-test'}))
    order_cardiac_xray = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input cardiac-test'}))

    class Meta:
        model = Screening
        fields = ['screening_notes']
        widgets = {
            'screening_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter screening notes...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['suspect_scd'].initial = self.instance.suspected_diseases.filter(code='SCD').exists()
            self.fields['suspect_dm'].initial = self.instance.suspected_diseases.filter(code='DM').exists()
            self.fields['suspect_cardiac'].initial = self.instance.suspected_diseases.filter(code='CARDIAC').exists()

            self.fields['order_scd_lab'].initial = self.instance.ordered_tests.filter(code='scd_lab').exists()
            self.fields['order_scd_radiology'].initial = self.instance.ordered_tests.filter(code='scd_xray').exists()
            self.fields['order_scd_echo'].initial = self.instance.ordered_tests.filter(code='scd_echo').exists()
            self.fields['order_scd_screening'].initial = self.instance.ordered_tests.filter(code='scd_screening').exists()

            self.fields['order_dm_hba1c'].initial = self.instance.ordered_tests.filter(code='hba1c').exists()
            self.fields['order_dm_c_peptide'].initial = self.instance.ordered_tests.filter(code='c_peptide').exists()
            self.fields['order_dm_creatinine'].initial = self.instance.ordered_tests.filter(code='creatinine').exists()
            self.fields['order_dm_urea'].initial = self.instance.ordered_tests.filter(code='urea').exists()
            self.fields['order_dm_rbg'].initial = self.instance.ordered_tests.filter(code='rbg').exists()
            self.fields['order_dm_fbg'].initial = self.instance.ordered_tests.filter(code='fbg').exists()

            self.fields['order_cardiac_lab'].initial = self.instance.ordered_tests.filter(code='cardiac_lab').exists()
            self.fields['order_cardiac_echo'].initial = self.instance.ordered_tests.filter(code='cardiac_echo').exists()
            self.fields['order_cardiac_ecg'].initial = self.instance.ordered_tests.filter(code='ecg').exists()
            self.fields['order_cardiac_xray'].initial = self.instance.ordered_tests.filter(code='cardiac_xray').exists()

    def save(self, commit=True):
        instance = super().save(commit=commit)
        
        from diseases.models import Disease
        from laboratory.models import LabTest

        diseases_to_add = []
        if self.cleaned_data.get('suspect_scd'):
            diseases_to_add.append(Disease.objects.get(code='SCD'))
        if self.cleaned_data.get('suspect_dm'):
            diseases_to_add.append(Disease.objects.get(code='DM'))
        if self.cleaned_data.get('suspect_cardiac'):
            diseases_to_add.append(Disease.objects.get(code='CARDIAC'))
            
        tests_to_add = []
        mapping = {
            'order_scd_lab': 'scd_lab',
            'order_scd_radiology': 'scd_xray',
            'order_scd_echo': 'scd_echo',
            'order_scd_screening': 'scd_screening',
            'order_dm_hba1c': 'hba1c',
            'order_dm_c_peptide': 'c_peptide',
            'order_dm_creatinine': 'creatinine',
            'order_dm_urea': 'urea',
            'order_dm_rbg': 'rbg',
            'order_dm_fbg': 'fbg',
            'order_cardiac_lab': 'cardiac_lab',
            'order_cardiac_echo': 'cardiac_echo',
            'order_cardiac_ecg': 'ecg',
            'order_cardiac_xray': 'cardiac_xray',
        }
        for field_name, test_code in mapping.items():
            if self.cleaned_data.get(field_name):
                try:
                    tests_to_add.append(LabTest.objects.get(code=test_code))
                except LabTest.DoesNotExist:
                    pass

        if not instance.pk:
            instance.save()
        instance.suspected_diseases.set(diseases_to_add)
        instance.ordered_tests.set(tests_to_add)
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
        from laboratory.models import PatientTestResult, LabTest
        if val is not None:
            test = LabTest.objects.get(code=code)
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
        from laboratory.models import PatientTestResult, LabTest
        if val is not None:
            test = LabTest.objects.get(code=code)
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
        from laboratory.models import PatientTestResult, LabTest
        if val is not None and val != '':
            test, _ = LabTest.objects.get_or_create(code=code, defaults={'name': code.replace('_', ' ').title(), 'category': 'cardiology'})
            res, _ = PatientTestResult.objects.get_or_create(patient=self.patient, test=test)
            res.result_value = str(val)
            if user and user.is_authenticated:
                res.updated_by = user
                res.created_by = user
            res.save()

class ConsultationForm(forms.ModelForm):
    confirmed_scd = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_confirmed_scd'}))
    confirmed_dm = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_confirmed_dm'}))
    confirmed_cardiac = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_confirmed_cardiac'}))

    class Meta:
        model = Consultation
        fields = ['diagnosis', 'confirmed_cardiac_type', 'comments']
        widgets = {
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Diagnosis...'}),
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
