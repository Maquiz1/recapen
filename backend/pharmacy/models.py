from django.db import models
from core.models import AuditableModel
from django.conf import settings

class InventoryBatch(AuditableModel):
    medication = models.ForeignKey('medications.Medication', on_delete=models.CASCADE, related_name='batches')
    batch_number = models.CharField(max_length=100)
    quantity_in_stock = models.PositiveIntegerField(default=0)
    expiration_date = models.DateField()
    received_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.medication.name} - Batch {self.batch_number}"

class Dispensation(AuditableModel):
    prescription = models.OneToOneField('clinical.Prescription', on_delete=models.CASCADE, related_name='dispensation', null=True, blank=True)
    dispensed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    dispensed_date = models.DateTimeField(auto_now_add=True)
    quantity_dispensed = models.PositiveIntegerField(help_text="Total number of pills, bottles, etc. dispensed")
    notes = models.TextField(blank=True, null=True, help_text="Pharmacist notes (e.g. substitutions, counseling given)")

    def __str__(self):
        return f"Dispensed {self.quantity_dispensed} of {self.prescription.medication.name} for {self.prescription.patient}"

class DispensationBatch(models.Model):
    dispensation = models.ForeignKey(Dispensation, on_delete=models.CASCADE, related_name='dispensation_batches')
    batch = models.ForeignKey(InventoryBatch, on_delete=models.CASCADE, related_name='dispensation_records')
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} from {self.batch}"
