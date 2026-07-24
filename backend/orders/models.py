from django.db import models
from django.conf import settings
from core.models import AuditableModel
from simple_history.models import HistoricalRecords
from patients.models import Patient
from encounters.models import Encounter
from diagnostics.models import DiagnosticTest

class Order(AuditableModel):
    ORDER_TYPE_CHOICES = (
        ('lab', 'Laboratory'),
        ('radiology', 'Radiology/Imaging'),
        ('cardiology', 'Cardiology'),
        ('pharmacy', 'Pharmacy/Medication'),
        ('other', 'Other'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    URGENCY_CHOICES = (
        ('routine', 'Routine'),
        ('urgent', 'Urgent'),
        ('stat', 'STAT (Immediate)'),
    )

    encounter = models.ForeignKey(Encounter, on_delete=models.CASCADE, related_name='orders')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='orders')
    ordering_doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='placed_orders')
    
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES)
    
    # For Lab/Rad/Cardio
    test = models.ForeignKey(DiagnosticTest, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    
    # For Pharmacy/Medications
    medication = models.ForeignKey('medications.Medication', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    dosage_instructions = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='routine')
    
    clinical_notes = models.TextField(blank=True, null=True, help_text="Reason for order or clinical context")
    order_date = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        item = self.test.test_name if self.test else (self.medication.name if self.medication else 'Unknown')
        return f"Order: {item} for {self.patient} ({self.get_status_display()})"
