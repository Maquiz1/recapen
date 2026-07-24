from django.db import models
from core.models import AuditableModel

class Disease(AuditableModel):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True, help_text="Short identifier e.g. SCD, DM, CARDIAC")
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.name
