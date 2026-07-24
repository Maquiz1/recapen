from django.db import models
from core.models import AuditableModel
from .categories import LaboratoryCategory, LaboratoryType

class LaboratoryTest(AuditableModel):
    name = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=50, unique=True, help_text="Unique slug e.g. hba1c, ecg, echo")
    # New LMS Fields
    laboratory_category = models.ForeignKey(LaboratoryCategory, on_delete=models.SET_NULL, blank=True, null=True, related_name='tests', help_text="Specific laboratory category")
    laboratory_type = models.ForeignKey(LaboratoryType, on_delete=models.SET_NULL, blank=True, null=True, related_name='tests', help_text="Specific laboratory type")
    range_min = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. '12.5', '0', 'Negative'")
    range_max = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. '18.0', '0', 'N/A'")
    units = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. 'g/dl', 'Reactive'")
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Cost of the test")
    
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    # Panel features
    is_panel = models.BooleanField(default=False, help_text="If True, this is a group of tests (e.g. BMP).")
    parent_panel = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_tests', help_text="If this test is part of a panel, link it here.")
    def __str__(self):
        return self.name
