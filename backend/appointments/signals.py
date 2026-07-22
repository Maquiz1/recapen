from django.db.models.signals import post_save
from django.dispatch import receiver
from patients.models import Enrollment, Patient
from appointments.services import generate_visits_for_patient

@receiver(post_save, sender=Enrollment)
def trigger_generation_on_enrollment(sender, instance, created, **kwargs):
    if created and instance.is_eligible:
        generate_visits_for_patient(instance.patient)

@receiver(post_save, sender=Patient)
def trigger_generation_on_patient_update(sender, instance, **kwargs):
    """
    Trigger generation if interval changes, or to halt/update if status changes.
    """
    if hasattr(instance, 'enrollment') and instance.enrollment.is_eligible:
        generate_visits_for_patient(instance)
