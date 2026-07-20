from django.db import models
from core.models import AuditableModel

class LabTest(AuditableModel):
    CATEGORY_CHOICES = (
        ('lab', 'Laboratory'),
        ('radiology', 'Radiology/Imaging'),
        ('cardiology', 'Cardiology'),
        ('other', 'Other'),
    )
    name = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=50, unique=True, help_text="Unique slug e.g. hba1c, ecg, echo")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='lab')
    diseases = models.ManyToManyField('diseases.Disease', related_name='lab_tests', blank=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class PatientTestResult(AuditableModel):
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='test_results')
    test = models.ForeignKey(LabTest, on_delete=models.CASCADE)
    result_value = models.CharField(max_length=255, blank=True, null=True, help_text="Entered lab result value")
    performed_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('patient', 'test')

    def __str__(self):
        return f"{self.patient} - {self.test}: {self.result_value}"
