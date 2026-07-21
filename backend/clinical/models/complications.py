from django.db import models
from core.models import AuditableModel
from encounters.models import Encounter

class Complications(AuditableModel):
    encounter = models.OneToOneField(Encounter, on_delete=models.CASCADE, related_name='complications')
    stroke = models.BooleanField(default=False)
    kidney_disease = models.BooleanField(default=False)
    retinopathy = models.BooleanField(default=False)
    neuropathy = models.BooleanField(default=False)
    diabetic_foot = models.BooleanField(default=False)
    cardiovascular_disease = models.BooleanField(default=False)
    other_complications = models.TextField(blank=True, null=True, help_text="Other complications details")

    class Meta:
        verbose_name_plural = "Complications"

    def __str__(self):
        return f"Complications for {self.encounter}"
