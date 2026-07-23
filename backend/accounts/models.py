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
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    role_type = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    def __str__(self):
        return f"{self.username} ({self.get_role_type_display() or 'No Role'})"
