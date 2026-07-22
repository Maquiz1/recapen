import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from patients.models import Patient, Enrollment
from appointments.models import Appointment
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import datetime

# Clean up
Patient.objects.filter(national_id="TEST_GEN_123").delete()

patient = Patient.objects.create(
    first_name="Test",
    last_name="Generation",
    date_of_birth=datetime.date(1990, 1, 1),
    gender="male",
    national_id="TEST_GEN_123",
    status="enrolled",
    follow_up_interval_months=1
)

# Backdate enrollment to 6 months ago
enrollment = Enrollment.objects.create(
    patient=patient,
    is_eligible=True,
    cohort="dm"
)
enrollment.enrollment_date = timezone.now().date() - relativedelta(months=6)
enrollment.save()

# Wait, the signal on Enrollment might have triggered already with today's date
# Let's delete the generated appointments and re-trigger manually after setting the date
Appointment.objects.filter(patient=patient).delete()

from appointments.services import generate_visits_for_patient
generate_visits_for_patient(patient)

visits = Appointment.objects.filter(patient=patient).order_by('visit_number')
print(f"Generated {visits.count()} visits.")
for v in visits:
    print(f"Visit {v.visit_number}: {v.scheduled_time.date()} - {v.status}")

