from django.db import models
from core.models import AuditableModel
from encounters.models import Encounter

class Treatment(AuditableModel):
    CHOICES_YN = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    encounter = models.OneToOneField(Encounter, on_delete=models.CASCADE, related_name='treatment')
    
    # Vaccination
    vaccination_needed = models.CharField(max_length=3, choices=CHOICES_YN, default='no')
    vaccination_which = models.CharField(max_length=255, blank=True, null=True)
    
    # Transfusions
    transfusion_needed = models.CharField(max_length=3, choices=CHOICES_YN, default='no')
    transfusion_units = models.IntegerField(default=0, blank=True, null=True)
    
    # Family Education
    education_diet = models.CharField(max_length=3, choices=CHOICES_YN, default='no')
    education_hydration = models.CharField(max_length=3, choices=CHOICES_YN, default='no')
    education_acute_symptoms = models.CharField(max_length=3, choices=CHOICES_YN, default='no')
    education_fever = models.CharField(max_length=3, choices=CHOICES_YN, default='no')
    education_lifestyle = models.CharField(max_length=3, choices=CHOICES_YN, default='no')
    education_misconception = models.CharField(max_length=3, choices=CHOICES_YN, default='no')
    
    # Support
    social_support_provided = models.CharField(max_length=3, choices=CHOICES_YN, default='no')
    social_support_type = models.CharField(max_length=255, blank=True, null=True)
    other_support_provided = models.CharField(max_length=3, choices=CHOICES_YN, default='no')
    other_support_specify = models.CharField(max_length=255, blank=True, null=True)
    referrals_provided = models.CharField(max_length=3, choices=CHOICES_YN, default='no')
    referrals_type = models.CharField(max_length=255, blank=True, null=True)
    
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Treatment Plan for {self.encounter}"
