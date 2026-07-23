from django.db import models
from core.models import AuditableModel
from simple_history.models import HistoricalRecords

class Medication(AuditableModel):
    FORM_CHOICES = (
        ('tablet', 'Tablet'),
        ('capsule', 'Capsule'),
        ('syrup', 'Syrup/Suspension'),
        ('injection', 'Injection'),
        ('cream', 'Cream/Ointment'),
        ('drops', 'Drops'),
        ('inhaler', 'Inhaler'),
        ('other', 'Other'),
    )
    
    name = models.CharField(max_length=150, unique=True, help_text="Brand or common name")
    generic_name = models.CharField(max_length=200, blank=True, null=True, help_text="Active ingredient(s)")
    form = models.CharField(max_length=20, choices=FORM_CHOICES, default='tablet')
    strength = models.CharField(max_length=100, help_text="e.g. 500mg, 10ml, etc.")
    stock_quantity = models.PositiveIntegerField(default=0, help_text="Current inventory stock level")
    reorder_level = models.PositiveIntegerField(default=20, help_text="Alert when stock falls below this level")
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True, help_text="Optional clinical notes or side effects")
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.name} ({self.strength} {self.get_form_display()})"
    
    class Meta:
        ordering = ['name']

