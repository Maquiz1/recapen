from django.db import models
from core.models import AuditableModel
from encounters.models import Encounter

class Symptom(AuditableModel):
    SEVERITY_CHOICES = [
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
    ]
    encounter = models.OneToOneField(Encounter, on_delete=models.CASCADE, related_name='symptom')
    reported_symptoms = models.TextField(blank=True, null=True, help_text="List of symptoms reported by the patient")
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    duration_days = models.IntegerField(blank=True, null=True, help_text="Symptom duration in days")

    def __str__(self):
        return f"Symptoms for {self.encounter}"
