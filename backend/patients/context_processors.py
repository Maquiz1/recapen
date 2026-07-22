from django.utils import timezone
from datetime import timedelta
from patients.models import Patient
from orders.models import Order
from django.db.models import Prefetch

def clinical_notifications_processor(request):
    """
    Identifies clinical missing data:
    1. Patients missing their 90-day HbA1c interval tests.
    2. Encounters missing medication prescriptions.
    """
    if not request.user.is_authenticated:
        return {'missing_hba1c_count': 0, 'missing_meds_count': 0}
        
    today = timezone.now().date()
    
    # 1. HbA1c check
    enrolled_patients = Patient.objects.filter(
        enrollment__isnull=False,
        is_deleted=False
    ).select_related('enrollment')
    
    missing_hba1c_count = 0
    for patient in enrolled_patients:
        if (today - patient.enrollment.enrollment_date).days >= 90:
            # Check their latest completed HbA1c test
            last_hba1c_order = Order.objects.filter(
                patient=patient,
                test__code__iexact='hba1c',
                status='completed'
            ).order_by('-updated_at').first()
            
            if not last_hba1c_order:
                missing_hba1c_count += 1
            else:
                last_result = last_hba1c_order.results.order_by('-performed_date').first()
                if last_result:
                    if (today - last_result.performed_date.date()).days > 90:
                        missing_hba1c_count += 1
                else:
                    missing_hba1c_count += 1

    # 2. Missing Medications Check
    # Find all encounters that do not have any associated orders with order_type='pharmacy'
    # We might only care about encounters that are active or arrived
    from encounters.models import Encounter
    missing_meds_encounters = Encounter.objects.exclude(prescriptions__isnull=False).distinct()
    missing_meds_count = missing_meds_encounters.count()
    
    return {
        'missing_hba1c_count': missing_hba1c_count,
        'missing_meds_count': missing_meds_count,
    }
