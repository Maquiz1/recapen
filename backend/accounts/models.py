from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('national', 'National Coordinator'),
        ('regional', 'Regional Coordinator'),
        ('district', 'District Coordinator'),
        ('facility', 'Facility Doctor/Nurse'),
        ('mentor', 'Mentor/Trainer'),
        ('pi', 'Principal Investigator'),
        ('clerk', 'Data Clerk'),
    )
    role_type = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_type_display() or 'No Role'})"
