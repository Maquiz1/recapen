from django.db import models
from django.conf import settings
from core.models import AuditableModel
from simple_history.models import HistoricalRecords
from patients.models import Patient

class Encounter(AuditableModel):
    ENCOUNTER_TYPE_CHOICES = (
        ('initial', 'Baseline'),
        ('followup', 'Follow-up'),
        ('emergency', 'Emergency'),
        ('routine', 'Routine Checkup'),
    )
    STATUS_CHOICES = (
        ('planned', 'Planned'),
        ('arrived', 'Arrived'),
        ('in_progress', 'In Progress'),
        ('finished', 'Finished'),
        ('cancelled', 'Cancelled'),
    )

    VISIT_NATURE_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('unscheduled', 'Unscheduled'),
    )

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='encounters')
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='encounters')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    encounter_type = models.CharField(max_length=20, choices=ENCOUNTER_TYPE_CHOICES, default='routine')
    visit_nature = models.CharField(max_length=20, choices=VISIT_NATURE_CHOICES, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='arrived')
    clinical_notes = models.TextField(blank=True, null=True, help_text="General notes for this encounter")
    history = HistoricalRecords()

    def __str__(self):
        return f"Encounter: {self.patient} on {self.start_time.strftime('%Y-%m-%d %H:%M')} ({self.get_status_display()})"
