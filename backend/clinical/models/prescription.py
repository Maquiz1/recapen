from django.db import models
from core.models import AuditableModel
from simple_history.models import HistoricalRecords

class Prescription(AuditableModel):
    ACTION_CHOICES = (
        ('continue', 'Continue'),
        ('stop', 'Stop'),
        ('new', 'New'),
        ('modify', 'Modify'),
    )
    encounter = models.ForeignKey('encounters.Encounter', on_delete=models.CASCADE, related_name='prescriptions')
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='prescriptions')
    medication = models.ForeignKey('medications.Medication', on_delete=models.CASCADE, related_name='prescriptions')
    
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True, help_text="If Stop")
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, default='continue')
    dose_description = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. 5, m, 1 tablet")
    dose_duration = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. 30, 60 days")
    
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.medication.name} for {self.patient}"

    class Meta:
        ordering = ['-start_date']
