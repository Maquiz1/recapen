import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from appointments.models import Appointment

def generate_visits_for_patient(patient):
    """
    Core engine to generate visits (Appointments) for a patient.
    Handles retrospective catch-up and prospective next-visit generation.
    """
    TERMINAL_STATUSES = ['died', 'ltfu', 'withdrawn', 'transferred', 'defaulted']
    if patient.status in TERMINAL_STATUSES:
        if patient.status_date:
            # Delete any scheduled visits that fall after the terminal date
            Appointment.objects.filter(
                patient=patient,
                scheduled_time__date__gt=patient.status_date,
                status='scheduled'
            ).delete()
        return

    # Must be enrolled
    if not hasattr(patient, 'enrollment'):
        return

    interval = patient.follow_up_interval_months
    if interval < 1:
        interval = 1

    enrollment_date = patient.enrollment.enrollment_date
    today = timezone.now().date()

    # Get existing visits
    existing_visits = Appointment.objects.filter(patient=patient, visit_nature='scheduled').order_by('-visit_number')
    
    if not existing_visits.exists():
        # First time generating visits
        # Create baseline (Baseline Assessment)
        baseline_dt = timezone.make_aware(timezone.datetime.combine(enrollment_date, datetime.time(9, 0)))
        Appointment.objects.create(
            patient=patient,
            scheduled_time=baseline_dt,
            reason='Baseline Visit',
            status='completed',
            visit_number=0,
            visit_nature='scheduled'
        )
        last_visit_date = enrollment_date
        next_visit_number = 1
    else:
        latest_visit = existing_visits.first()
        last_visit_date = latest_visit.scheduled_time.date()
        next_visit_number = (latest_visit.visit_number or 0) + 1

    # Generate up to today + 1 interval
    while True:
        next_date = last_visit_date + relativedelta(months=interval)
        
        # Stop generating if the next_date is more than one interval past today
        if next_date > today + relativedelta(months=interval):
            break
            
        # Is the generated visit in the past?
        if next_date < today:
            status = 'missed'
        else:
            status = 'scheduled'

        scheduled_dt = timezone.make_aware(timezone.datetime.combine(next_date, datetime.time(9, 0)))
        
        # Prevent duplicates by checking if a scheduled visit already exists for this specific month/year
        if not Appointment.objects.filter(
            patient=patient, 
            visit_nature='scheduled',
            scheduled_time__year=next_date.year,
            scheduled_time__month=next_date.month
        ).exists():
            Appointment.objects.create(
                patient=patient,
                scheduled_time=scheduled_dt,
                reason=f'Visit {next_visit_number}',
                status=status,
                visit_number=next_visit_number,
                visit_nature='scheduled'
            )
            
        last_visit_date = next_date
        next_visit_number += 1
