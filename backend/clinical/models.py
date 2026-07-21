from django.db import models
from core.models import AuditableModel
from encounters.models import Encounter

class Vitals(AuditableModel):
    encounter = models.OneToOneField(Encounter, on_delete=models.CASCADE, related_name='vitals')
    blood_pressure_systolic = models.IntegerField(null=True, blank=True)
    blood_pressure_diastolic = models.IntegerField(null=True, blank=True)
    heart_rate = models.IntegerField(null=True, blank=True, help_text="BPM")
    oxygen_saturation = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="%")
    pain_score = models.IntegerField(null=True, blank=True, help_text="0-10 scale")
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Vitals for {self.encounter}"

class Hospitalization(AuditableModel):
    encounter = models.OneToOneField(Encounter, on_delete=models.CASCADE, related_name='hospitalization')
    admission_date = models.DateField(null=True, blank=True)
    discharge_date = models.DateField(null=True, blank=True)
    reason_for_admission = models.CharField(max_length=255, null=True, blank=True)
    ward = models.CharField(max_length=100, null=True, blank=True)
    outcome = models.CharField(max_length=50, choices=[
        ('discharged', 'Discharged Home'),
        ('transferred', 'Transferred to another facility'),
        ('died', 'Died'),
        ('ama', 'Discharged AMA (Against Medical Advice)'),
        ('other', 'Other'),
    ], null=True, blank=True)
    discharge_summary = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Hospitalization for {self.encounter}"

class Risk(AuditableModel):
    SMOKING_CHOICES = [
        ('never', 'Never Smoked'),
        ('current', 'Current Smoker'),
        ('former', 'Former Smoker'),
    ]
    encounter = models.OneToOneField(Encounter, on_delete=models.CASCADE, related_name='risk')
    smoking_status = models.CharField(max_length=20, choices=SMOKING_CHOICES, default='never')
    alcohol_use = models.BooleanField(default=False)
    physical_inactivity = models.BooleanField(default=False, help_text="Less than 150 mins of moderate activity per week")
    family_history_ncd = models.BooleanField(default=False, help_text="Family history of Hypertension, Diabetes, or Heart Disease")
    unhealthy_diet = models.BooleanField(default=False)

    def __str__(self):
        return f"Risk Factors for {self.encounter}"

class Socioeconomic(AuditableModel):
    EDUCATION_CHOICES = [
        ('none', 'No formal education'),
        ('primary', 'Primary education'),
        ('secondary', 'Secondary education'),
        ('higher', 'Higher education'),
    ]
    EMPLOYMENT_CHOICES = [
        ('employed', 'Employed'),
        ('unemployed', 'Unemployed'),
        ('student', 'Student'),
        ('retired', 'Retired'),
        ('other', 'Other'),
    ]
    encounter = models.OneToOneField(Encounter, on_delete=models.CASCADE, related_name='socioeconomic')
    education_level = models.CharField(max_length=20, choices=EDUCATION_CHOICES, default='none')
    employment_status = models.CharField(max_length=20, choices=EMPLOYMENT_CHOICES, default='other')
    monthly_income = models.CharField(max_length=50, blank=True, null=True, help_text="Estimated monthly household income")
    access_clean_water = models.BooleanField(default=True)
    has_health_insurance = models.BooleanField(default=False)

    def __str__(self):
        return f"Socioeconomic Factors for {self.encounter}"

class Treatment(AuditableModel):
    CHOICES_YN = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    encounter = models.OneToOneField(Encounter, on_delete=models.CASCADE, related_name='treatment')
    
    # Vaccination
    vaccination_needed = models.CharField(max_length=3, choices=CHOICES_YN, default='no')
    vaccination_which = models.CharField(max_length=255, blank=True, null=True)
    
    # Transfusions
    transfusion_needed = models.CharField(max_length=3, choices=CHOICES_YN, default='no')
    transfusion_units = models.IntegerField(default=0, blank=True, null=True)
    
    # Family Education
    education_diet = models.CharField(max_length=3, choices=CHOICES_YN, default='no')
    education_hydration = models.CharField(max_length=3, choices=CHOICES_YN, default='no')
    education_acute_symptoms = models.CharField(max_length=3, choices=CHOICES_YN, default='no')
    education_fever = models.CharField(max_length=3, choices=CHOICES_YN, default='no')
    education_lifestyle = models.CharField(max_length=3, choices=CHOICES_YN, default='no')
    education_misconception = models.CharField(max_length=3, choices=CHOICES_YN, default='no')
    
    # Support
    social_support_provided = models.CharField(max_length=3, choices=CHOICES_YN, default='no')
    social_support_type = models.CharField(max_length=255, blank=True, null=True)
    other_support_provided = models.CharField(max_length=3, choices=CHOICES_YN, default='no')
    other_support_specify = models.CharField(max_length=255, blank=True, null=True)
    referrals_provided = models.CharField(max_length=3, choices=CHOICES_YN, default='no')
    referrals_type = models.CharField(max_length=255, blank=True, null=True)
    
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Treatment Plan for {self.encounter}"
