from django.db import models
from core.models import AuditableModel

class Department(AuditableModel):
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(blank=True, null=True)
    head = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
