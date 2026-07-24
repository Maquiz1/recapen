from django.db import models
from core.models import AuditableModel
from departments.models import Department

class DiagnosticGroup(AuditableModel):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='diagnostic_groups', help_text="Department this group belongs to")
    name = models.CharField(max_length=150, unique=True, help_text="e.g. X-ray, Haematology")
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.department.name})"

class DiagnosticCategory(AuditableModel):
    group = models.ForeignKey(DiagnosticGroup, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['group', 'name']
        verbose_name_plural = "Diagnostic Categories"

    def __str__(self):
        return f"{self.group.name} - {self.name}"

class DiagnosticTest(AuditableModel):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='diagnostic_tests', help_text="Department this test belongs to")
    test_name = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=50, unique=True, help_text="Unique slug e.g. hba1c, ecg, echo")
    
    diagnostic_group = models.ForeignKey(DiagnosticGroup, on_delete=models.SET_NULL, blank=True, null=True, related_name='tests', help_text="Specific diagnostic group")
    diagnostic_category = models.ForeignKey(DiagnosticCategory, on_delete=models.SET_NULL, blank=True, null=True, related_name='tests', help_text="Specific diagnostic category")
    
    range_min = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. '12.5', '0', 'Negative'")
    range_max = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. '18.0', '0', 'N/A'")
    units = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. 'g/dl', 'Reactive'")
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Cost of the test")
    
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.test_name
