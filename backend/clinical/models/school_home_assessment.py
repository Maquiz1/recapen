from django.db import models
from core.models import AuditableModel
from encounters.models import Encounter

class SchoolHomeAssessment(AuditableModel):
    CHOICES_YN = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    
    REFERRAL_CHOICES = [
        ('inpatient', 'Inpatient / hospital stay'),
        ('primary', 'Primary care clinic'),
        ('outpatient', 'Other outpatient clinic'),
        ('maternal', 'Maternal health'),
        ('community', 'Community'),
        ('self', 'Self'),
        ('other', 'Other'),
    ]
    
    encounter = models.OneToOneField(Encounter, on_delete=models.CASCADE, related_name='school_home_assessment')
    visit_date = models.DateField(null=True, blank=True)
    appropriate_grade_for_age = models.CharField(max_length=3, choices=CHOICES_YN, default='no')
    ncd_limiting_school = models.CharField(max_length=3, choices=CHOICES_YN, default='no')
    school_days_missed = models.IntegerField(null=True, blank=True, help_text="Days of missed school in past month")
    household_size = models.IntegerField(null=True, blank=True)
    referred_from = models.CharField(max_length=20, choices=REFERRAL_CHOICES, default='other')
    agrees_to_home_visits = models.CharField(max_length=3, choices=CHOICES_YN, default='no')
    chw_name_available = models.CharField(max_length=3, choices=CHOICES_YN, default='no')
    chw_name = models.TextField(blank=True, null=True, help_text="CHW Name Details")
    general_comments = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "School & Home Assessment"
        verbose_name_plural = "School & Home Assessments"

    def __str__(self):
        return f"School & Home Assessment for {self.encounter}"
