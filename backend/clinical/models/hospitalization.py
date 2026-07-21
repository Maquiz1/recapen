from django.db import models
from core.models import AuditableModel
from encounters.models import Encounter

class Hospitalization(AuditableModel):
    CHOICES_YN = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    CHOICES_YN_NA = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('na', 'N/A'),
    ]
    
    encounter = models.OneToOneField(Encounter, on_delete=models.CASCADE, related_name='hospitalization')
    
    # Hospitalization
    recent_hospitalizations = models.CharField(max_length=3, choices=CHOICES_YN, default='no')
    num_hospitalizations_12m = models.IntegerField(default=0, help_text="(N/A = 98), (Missing = 99)")
    for_ncd = models.CharField(max_length=5, choices=[('yes', 'Yes'), ('no', 'No'), ('unset', 'Unset')], default='unset')
    num_hospitalizations_ncd_12m = models.IntegerField(default=0, help_text="(N/A = 98), (Missing = 99)")
    
    # School
    school_days_missed_last_month = models.IntegerField(default=0, help_text="(N/A = 98), (Missing = 99)")
    
    # Transfusion
    transfusions_past_month = models.IntegerField(default=0, help_text="(N/A = 98), (Missing = 99)")
    
    # Management at Home
    taking_malaria_prophylaxis = models.CharField(max_length=3, choices=CHOICES_YN_NA, default='na')
    taking_insecticide_net = models.CharField(max_length=3, choices=CHOICES_YN_NA, default='na')
    taking_folic_acid = models.CharField(max_length=3, choices=CHOICES_YN_NA, default='na')
    taking_penicillin_prophylaxis = models.CharField(max_length=3, choices=CHOICES_YN_NA, default='na')
    pneumococcal_vaccination_up_to_date = models.CharField(max_length=3, choices=CHOICES_YN_NA, default='na')
    on_chronic_opioid_therapy = models.CharField(max_length=3, choices=CHOICES_YN_NA, default='na')
    
    on_hydroxyurea = models.CharField(max_length=3, choices=CHOICES_YN_NA, default='na')
    hydroxyurea_start_date = models.DateField(null=True, blank=True)
    hydroxyurea_dose = models.IntegerField(default=0, blank=True, null=True, help_text="(N/A = 98), (Missing = 99)")

    def __str__(self):
        return f"Hospitalization, School and Management at Home for {self.encounter}"
