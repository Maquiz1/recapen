from django.db import models
from core.models import AuditableModel
from encounters.models import Encounter

class History(AuditableModel):
    encounter = models.OneToOneField(Encounter, on_delete=models.CASCADE, related_name='history')
    medical_history = models.TextField(blank=True, null=True, help_text="Past medical history details")
    family_history = models.TextField(blank=True, null=True, help_text="Family history details")
    surgical_history = models.TextField(blank=True, null=True, help_text="Past surgical history")

    class Meta:
        verbose_name_plural = "Histories"

    def __str__(self):
        return f"History for {self.encounter}"
