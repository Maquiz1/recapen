from django.db import models
from core.models import AuditableModel
from patients.models import Enrollment

class SickleCellBaseline(AuditableModel):
    DIAGNOSIS_CHOICES = (
        ('scd', 'Sickle Cell Disease'),
        ('other', 'Other Hemoglobinopathy'),
    )
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='scd_baseline')
    visit_date = models.DateField(blank=True, null=True)
    diagnosis_date = models.DateField(blank=True, null=True)
    main_diagnosis = models.CharField(max_length=20, choices=DIAGNOSIS_CHOICES, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"SCD Baseline for {self.enrollment.patient}"

class DiabetesBaseline(AuditableModel):
    DIAGNOSIS_CHOICES = (
        ('type1', 'Type 1 DM'),
        ('type2', 'Type 2 DM'),
        ('gestational', 'Gestational DM'),
        ('unspecified', 'DM not yet specified'),
        ('other', 'Other'),
    )
    PRESENTATION_CHOICES = (
        ('dka_coma', 'DKA with coma'),
        ('dka_no_coma', 'DKA without coma'),
        ('ketosis', 'Ketosis'),
        ('hyperglycemia', 'Hyperglycemia'),
        ('screening', 'By Screening'),
        ('none', 'None'),
    )
    HYPERTENSION_CHOICES = (
        ('yes', 'Yes'),
        ('no', 'No'),
        ('unknown', 'Unknown'),
    )
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='dm_baseline')
    visit_date = models.DateField(blank=True, null=True)
    diagnosis_date = models.DateField(blank=True, null=True)
    main_diagnosis = models.CharField(max_length=20, choices=DIAGNOSIS_CHOICES, blank=True, null=True)
    presentation = models.CharField(max_length=20, choices=PRESENTATION_CHOICES, blank=True, null=True)
    hypertension = models.CharField(max_length=10, choices=HYPERTENSION_CHOICES, blank=True, null=True)
    hypertension_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"DM Baseline for {self.enrollment.patient}"


class CardiacBaseline(AuditableModel):
    YES_NO_CHOICES = (
        ('yes', 'Yes'),
        ('no', 'No'),
    )
    CARDIOMYOPATHY_CHOICES = (
        ('ischemic', 'Ischemic'),
        ('alcohol', 'Alcohol-related'),
        ('peripartum', 'Peripartum'),
        ('arrhythmia', 'Arrhythmia-related'),
        ('hiv', 'HIV-related'),
        ('chemotherapy', 'Chemotherapy-related'),
        ('viral', 'Viral/idiopathic'),
        ('other', 'Other'),
    )
    RHD_CHOICES = (
        ('ms', 'Pure mitral stenosis'),
        ('mr', 'Pure mitral regurgitation'),
        ('mixed_mitral', 'Mixed mitral valve disease (MS + MR)'),
        ('avd', 'Isolated aortic valve disease (AVD)'),
        ('mmavd', 'Mixed mitral and aortic valve disease (MMAVD)'),
        ('other', 'Other'),
    )
    CHD_CHOICES = (
        ('asd', 'ASD'),
        ('vsd', 'VSD'),
        ('pda', 'PDA'),
        ('coarctation', 'Coarctation of aorta'),
        ('tetralogy', 'Tetralogy of Fallot'),
        ('other', 'Other'),
    )
    RHF_CHOICES = (
        ('cld', 'Chronic Lung Disease'),
        ('other', 'Other'),
    )
    PERICARDIAL_CHOICES = (
        ('tb', 'Tuberculosis'),
        ('hiv', 'HIV'),
        ('malignancy', 'Malignancy'),
        ('other', 'Other'),
    )
    STROKE_CHOICES = (
        ('ischemic', 'Ischemic'),
        ('hemorrhagic', 'Hemorrhagic'),
        ('unknown', 'Unknown'),
    )
    ARRHYTHMIA_CHOICES = (
        ('af', 'Atrial fibrillation'),
        ('other', 'Other'),
    )
    THROMBO_CHOICES = (
        ('pe', 'Pulmonary embolism'),
        ('dvt', 'DVT'),
        ('other', 'Other'),
    )

    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='cardiac_baseline')
    visit_date = models.DateField(blank=True, null=True)
    diagnosis_date = models.DateField(blank=True, null=True)
    
    hypertensive_heart_disease = models.CharField(max_length=10, choices=YES_NO_CHOICES, blank=True, null=True)
    coronary_artery_disease = models.CharField(max_length=10, choices=YES_NO_CHOICES, blank=True, null=True)
    severe_uncontrolled_hypertension = models.CharField(max_length=10, choices=YES_NO_CHOICES, blank=True, null=True)

    cardiomyopathy = models.CharField(max_length=10, choices=YES_NO_CHOICES, blank=True, null=True)
    cardiomyopathy_type = models.CharField(max_length=20, choices=CARDIOMYOPATHY_CHOICES, blank=True, null=True)
    cardiomyopathy_other = models.TextField(blank=True, null=True)

    rheumatic_heart_disease = models.CharField(max_length=10, choices=YES_NO_CHOICES, blank=True, null=True)
    rhd_type = models.CharField(max_length=20, choices=RHD_CHOICES, blank=True, null=True)

    congenital_heart_disease = models.CharField(max_length=10, choices=YES_NO_CHOICES, blank=True, null=True)
    chd_type = models.CharField(max_length=20, choices=CHD_CHOICES, blank=True, null=True)

    right_heart_failure = models.CharField(max_length=10, choices=YES_NO_CHOICES, blank=True, null=True)
    right_heart_failure_type = models.CharField(max_length=20, choices=RHF_CHOICES, blank=True, null=True)

    pericardial_disease = models.CharField(max_length=10, choices=YES_NO_CHOICES, blank=True, null=True)
    pericardial_disease_type = models.CharField(max_length=20, choices=PERICARDIAL_CHOICES, blank=True, null=True)

    stroke = models.CharField(max_length=10, choices=YES_NO_CHOICES, blank=True, null=True)
    stroke_type = models.CharField(max_length=20, choices=STROKE_CHOICES, blank=True, null=True)

    arrhythmia = models.CharField(max_length=10, choices=YES_NO_CHOICES, blank=True, null=True)
    arrhythmia_type = models.CharField(max_length=20, choices=ARRHYTHMIA_CHOICES, blank=True, null=True)

    thromboembolic = models.CharField(max_length=10, choices=YES_NO_CHOICES, blank=True, null=True)
    thromboembolic_type = models.CharField(max_length=20, choices=THROMBO_CHOICES, blank=True, null=True)

    any_other_diagnosis = models.CharField(max_length=10, choices=YES_NO_CHOICES, blank=True, null=True)
    other_diagnosis_specify = models.TextField(blank=True, null=True)
    general_comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Cardiac Baseline for {self.enrollment.patient}"
