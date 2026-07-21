from django.db import models
from core.models import AuditableModel
from encounters.models import Encounter

class Socioeconomic(AuditableModel):
    EDUCATION_CHOICES = [
        ('none', 'No formal education'),
        ('primary', 'Primary education'),
        ('secondary', 'Secondary education'),
        ('higher', 'Higher education'),
    ]
    EMPLOYMENT_CHOICES = [
        ('employed', 'Employed'),
        ('unemployed', 'Unemployed'),
        ('student', 'Student'),
        ('retired', 'Retired'),
        ('other', 'Other'),
    ]
    encounter = models.OneToOneField(Encounter, on_delete=models.CASCADE, related_name='socioeconomic')
    education_level = models.CharField(max_length=20, choices=EDUCATION_CHOICES, default='none')
    employment_status = models.CharField(max_length=20, choices=EMPLOYMENT_CHOICES, default='other')
    monthly_income = models.CharField(max_length=50, blank=True, null=True, help_text="Estimated monthly household income")
    access_clean_water = models.BooleanField(default=True)
    has_health_insurance = models.BooleanField(default=False)

    def __str__(self):
        return f"Socioeconomic Factors for {self.encounter}"
