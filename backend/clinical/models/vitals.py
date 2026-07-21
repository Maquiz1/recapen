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
