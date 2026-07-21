from django.db import models
from core.models import AuditableModel
from encounters.models import Encounter

class Risk(AuditableModel):
    TOBACCO_CHOICES = [
        ('never', 'Never'),
        ('current', 'Current'),
        ('former', 'Former'),
    ]
    ALCOHOL_CHOICES = [
        ('never', 'Never'),
        ('current', 'Current'),
        ('former', 'Former'),
    ]
    EMPLOYMENT_CHOICES = [
        ('student', 'Student'),
        ('employed', 'Employed'),
        ('unemployed', 'Unemployed'),
        ('retired', 'Retired'),
        ('other', 'Other'),
    ]
    YN_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    HIV_CHOICES = [
        ('r', 'R (Reactive)'),
        ('nr', 'NR (Non-Reactive)'),
        ('unknown', 'Unknown'),
    ]
    TB_CHOICES = [
        ('positive', 'Positive: Smear / Xpert / Other'),
        ('negative', 'Negative: Smear / Xpert / Other'),
        ('eptb', 'EPTB'),
        ('unknown', 'Unknown'),
    ]

    encounter = models.OneToOneField(Encounter, on_delete=models.CASCADE, related_name='risk')
    tobacco = models.CharField(max_length=20, choices=TOBACCO_CHOICES, default='never')
    alcohol = models.CharField(max_length=20, choices=ALCOHOL_CHOICES, default='never')
    employment_status = models.CharField(max_length=20, choices=EMPLOYMENT_CHOICES, default='other')
    ncd_limiting_school = models.CharField(max_length=3, choices=YN_CHOICES, default='no')
    
    # HIV
    hiv_status = models.CharField(max_length=10, choices=HIV_CHOICES, default='unknown')
    
    # TB
    tb_status = models.CharField(max_length=20, choices=TB_CHOICES, default='unknown')
    tb_screening_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Risk Factors for {self.encounter}"
