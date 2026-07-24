from django.db import models
from core.models import AuditableModel

class LaboratoryCategory(AuditableModel):
    name = models.CharField(max_length=150, unique=True, help_text="e.g. Haematology, Clinical Chemistry")
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Laboratory Categories"

    def __str__(self):
        return self.name

class LaboratoryType(AuditableModel):
    category = models.ForeignKey(LaboratoryCategory, on_delete=models.CASCADE, related_name='types')
    name = models.CharField(max_length=150, help_text="e.g. Renal Function Test")
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Laboratory Types"
        unique_together = ('category', 'name')

    def __str__(self):
        return f"{self.category.name} - {self.name}"
