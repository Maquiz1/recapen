from django.db import models
from core.models import AuditableModel
from simple_history.models import HistoricalRecords

MARITAL_STATUS_CHOICES = (
    ('single', 'Single'),
    ('married', 'Married'),
    ('divorced', 'Divorced'),
    ('widowed', 'Widowed'),
)

CARDIAC_TYPE_CHOICES = (
    ('rhd', 'RHD (Rheumatic Heart Disease)'),
    ('chd', 'CHD (Congenital Heart Disease)'),
    ('hf', 'HF (Heart Failure)'),
    ('arth', 'ARTH (Arrhythmia)'),
)

class Patient(AuditableModel):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    STATUS_CHOICES = (
        ('registered', 'Registered'),
        ('screened', 'Screened'),
        ('diagnosed', 'Diagnosed'),
        ('enrolled', 'Enrolled'),
        ('ineligible', 'Ineligible'),
        ('died', 'Deceased'),
        ('ltfu', 'Loss to Follow-Up'),
        ('withdrawn', 'Withdrawn Consent'),
        ('transferred', 'Transferred Out'),
        ('defaulted', 'Defaulted'),
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    national_id = models.CharField(max_length=50, blank=True, null=True, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')
    status_date = models.DateField(null=True, blank=True, help_text="Date of death, LTFU, or transfer")
    id_number = models.CharField(max_length=50, blank=True, null=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, default='single')
    follow_up_interval_months = models.IntegerField(default=1, help_text="Follow-up interval in months")
    passport_size_photo = models.ImageField(upload_to='patient_photos/', blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def scd_investigation(self):
        class SCDInvestigationWrapper:
            def __init__(self, patient):
                self.patient = patient
            @property
            def lab_results(self):
                res = self.patient.test_results.filter(test__code='scd_lab').first()
                return res.result_value if res else ''
            @property
            def radiology_results(self):
                res = self.patient.test_results.filter(test__code='scd_xray').first()
                return res.result_value if res else ''
            @property
            def echo_results(self):
                res = self.patient.test_results.filter(test__code='scd_echo').first()
                return res.result_value if res else ''
            @property
            def scd_screening_results(self):
                res = self.patient.test_results.filter(test__code='scd_screening').first()
                return res.result_value if res else ''
        return SCDInvestigationWrapper(self)

    @property
    def dm_investigation(self):
        class DMInvestigationWrapper:
            def __init__(self, patient):
                self.patient = patient
            @property
            def hba1c(self):
                res = self.patient.test_results.filter(test__code='hba1c').first()
                return float(res.result_value) if res and res.result_value else None
            @property
            def c_peptide(self):
                res = self.patient.test_results.filter(test__code='c_peptide').first()
                return float(res.result_value) if res and res.result_value else None
            @property
            def creatinine(self):
                res = self.patient.test_results.filter(test__code='creatinine').first()
                return float(res.result_value) if res and res.result_value else None
            @property
            def urea(self):
                res = self.patient.test_results.filter(test__code='urea').first()
                return float(res.result_value) if res and res.result_value else None
            @property
            def rbg(self):
                res = self.patient.test_results.filter(test__code='rbg').first()
                return float(res.result_value) if res and res.result_value else None
            @property
            def fbg(self):
                res = self.patient.test_results.filter(test__code='fbg').first()
                return float(res.result_value) if res and res.result_value else None
        return DMInvestigationWrapper(self)

    @property
    def cardiac_investigation(self):
        class CardiacInvestigationWrapper:
            def __init__(self, patient):
                self.patient = patient
            @property
            def cardiac_type(self):
                res = self.patient.test_results.filter(test__code='cardiac_type').first()
                return res.result_value if res else ''
            def get_cardiac_type_display(self):
                val = self.cardiac_type
                choices_dict = dict(CARDIAC_TYPE_CHOICES)
                return choices_dict.get(val, val)
            @property
            def lab_results(self):
                res = self.patient.test_results.filter(test__code='cardiac_lab').first()
                return res.result_value if res else ''
            @property
            def echo_results(self):
                res = self.patient.test_results.filter(test__code='cardiac_echo').first()
                return res.result_value if res else ''
            @property
            def ecg_results(self):
                res = self.patient.test_results.filter(test__code='ecg').first()
                return res.result_value if res else ''
            @property
            def xray_results(self):
                res = self.patient.test_results.filter(test__code='cardiac_xray').first()
                return res.result_value if res else ''
        return CardiacInvestigationWrapper(self)

class Screening(AuditableModel):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='screening')
    suspected_diseases = models.ManyToManyField('diseases.Disease', blank=True, related_name='screenings')
    ordered_tests = models.ManyToManyField('laboratory.LabTest', blank=True, related_name='screening_orders')
    screening_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Screening for {self.patient}"

    @property
    def suspect_scd(self):
        return self.suspected_diseases.filter(code='SCD').exists()
        
    @property
    def suspect_dm(self):
        return self.suspected_diseases.filter(code='DM').exists()
        
    @property
    def suspect_cardiac(self):
        return self.suspected_diseases.filter(code='CARDIAC').exists()

    @property
    def order_scd_lab(self):
        return self.ordered_tests.filter(code='scd_lab').exists()
    @property
    def order_scd_radiology(self):
        return self.ordered_tests.filter(code='scd_xray').exists()
    @property
    def order_scd_echo(self):
        return self.ordered_tests.filter(code='scd_echo').exists()
    @property
    def order_scd_screening(self):
        return self.ordered_tests.filter(code='scd_screening').exists()

    @property
    def order_dm_hba1c(self):
        return self.ordered_tests.filter(code='hba1c').exists()
    @property
    def order_dm_c_peptide(self):
        return self.ordered_tests.filter(code='c_peptide').exists()
    @property
    def order_dm_creatinine(self):
        return self.ordered_tests.filter(code='creatinine').exists()
    @property
    def order_dm_urea(self):
        return self.ordered_tests.filter(code='urea').exists()
    @property
    def order_dm_rbg(self):
        return self.ordered_tests.filter(code='rbg').exists()
    @property
    def order_dm_fbg(self):
        return self.ordered_tests.filter(code='fbg').exists()

    @property
    def order_cardiac_lab(self):
        return self.ordered_tests.filter(code='cardiac_lab').exists()
    @property
    def order_cardiac_echo(self):
        return self.ordered_tests.filter(code='cardiac_echo').exists()
    @property
    def order_cardiac_ecg(self):
        return self.ordered_tests.filter(code='ecg').exists()
    @property
    def order_cardiac_xray(self):
        return self.ordered_tests.filter(code='cardiac_xray').exists()

class Diagnosis(AuditableModel):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='diagnosis')
    diagnosis = models.TextField()
    confirmed_diseases = models.ManyToManyField('diseases.Disease', blank=True, related_name='diagnoses')
    confirmed_cardiac_type = models.CharField(max_length=20, choices=CARDIAC_TYPE_CHOICES, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Diagnosis for {self.patient}"

    @property
    def confirmed_scd(self):
        return self.confirmed_diseases.filter(code='SCD').exists()
        
    @property
    def confirmed_dm(self):
        return self.confirmed_diseases.filter(code='DM').exists()
        
    @property
    def confirmed_cardiac(self):
        return self.confirmed_diseases.filter(code='CARDIAC').exists()

class Enrollment(AuditableModel):
    COHORT_CHOICES = (
        ('cardiac', 'Cardiac'),
        ('scd', 'SCD'),
        ('dm', 'DM'),
    )
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='enrollment')
    is_eligible = models.BooleanField(default=True)
    cohort = models.CharField(max_length=20, choices=COHORT_CHOICES, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True, help_text="Explanation if not eligible")
    enrollment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Enrollment for {self.patient} ({self.cohort or 'Not Enrolled'})"
