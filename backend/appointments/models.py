from django.db import models
from core.models import AuditableModel
from django.conf import settings

class Appointment(AuditableModel):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('arrived', 'Arrived / Checked-In'),
        ('cancelled', 'Cancelled'),
        ('missed', 'Missed'),
        ('not_applicable', 'Not Applicable'),
        ('completed', 'Completed'),
    )
    
    VISIT_NATURE_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('unscheduled', 'Unscheduled'),
    )
    
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    scheduled_time = models.DateTimeField()
    reason = models.CharField(max_length=255, help_text="Reason for visit")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    encounter = models.OneToOneField('encounters.Encounter', on_delete=models.SET_NULL, null=True, blank=True, related_name='appointment')
    visit_number = models.IntegerField(null=True, blank=True, help_text="0 for Baseline, 1 for Visit 1, etc.")
    visit_nature = models.CharField(max_length=20, choices=VISIT_NATURE_CHOICES, default='scheduled')
    
    class Meta:
        ordering = ['scheduled_time']

    def __str__(self):
        return f"{self.patient} at {self.scheduled_time.strftime('%Y-%m-%d %H:%M')}"
