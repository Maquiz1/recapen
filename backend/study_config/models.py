from django.db import models
from core.models import AuditableModel

class ClinicalForm(AuditableModel):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50, unique=True, help_text="Internal code for the form (e.g. scd_vitals)")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class FollowUpRule(AuditableModel):
    COHORT_CHOICES = (
        ('cardiac', 'Cardiac'),
        ('scd', 'SCD'),
        ('dm', 'DM'),
    )
    VISIT_NATURE_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('unscheduled', 'Unscheduled'),
    )
    
    cohort = models.CharField(max_length=20, choices=COHORT_CHOICES)
    visit_nature = models.CharField(max_length=20, choices=VISIT_NATURE_CHOICES)
    required_forms = models.ManyToManyField(ClinicalForm, related_name='rules', blank=True)
    
    class Meta:
        unique_together = ('cohort', 'visit_nature')

    def __str__(self):
        return f"{self.get_cohort_display()} - {self.get_visit_nature_display()} Rule"
