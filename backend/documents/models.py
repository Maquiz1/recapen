from django.db import models
from core.models import AuditableModel
from django.conf import settings
import os

def patient_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/patients/patient_<id>/<filename>
    return f'patients/patient_{instance.patient.pk}/{filename}'

class PatientDocument(AuditableModel):
    DOCUMENT_TYPES = (
        ('id_scan', 'ID Scan / Passport'),
        ('outside_lab_report', 'Outside Lab Report'),
        ('consent_form', 'Consent Form'),
        ('referral_letter', 'Referral Letter'),
        ('insurance_card', 'Insurance Card'),
        ('other', 'Other'),
    )

    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='documents')
    encounter = models.ForeignKey('encounters.Encounter', on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    file = models.FileField(upload_to=patient_directory_path)
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES, default='other')
    description = models.CharField(max_length=255, blank=True, null=True, help_text="Optional description of the file")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.get_document_type_display()} for {self.patient}"
    
    @property
    def filename(self):
        return os.path.basename(self.file.name)
