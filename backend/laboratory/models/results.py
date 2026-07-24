from django.db import models
from django.conf import settings
from core.models import AuditableModel
from diagnostics.models import DiagnosticTest

class PatientTestResult(AuditableModel):
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='test_results')
    test = models.ForeignKey(DiagnosticTest, on_delete=models.CASCADE)
    order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True, blank=True, related_name='results')
    result_value = models.CharField(max_length=255, blank=True, null=True, help_text="Entered lab result value")
    flag = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. High, Low, Critical")
    notes = models.TextField(blank=True, null=True, help_text="Lab tech comments")
    entered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    performed_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.test.test_name} for {self.patient}: {self.result_value}"
