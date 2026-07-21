from django.db import models
from core.models import AuditableModel
from django.conf import settings

class Dispensation(AuditableModel):
    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, related_name='dispensation')
    dispensed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    dispensed_date = models.DateTimeField(auto_now_add=True)
    quantity_dispensed = models.PositiveIntegerField(help_text="Number of pills, bottles, etc.")
    notes = models.TextField(blank=True, null=True, help_text="Pharmacist notes (e.g. substitutions, counseling given)")

    def __str__(self):
        return f"Dispensed {self.quantity_dispensed} of {self.order.medication.name} for {self.order.patient}"
