import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from patients.models import Diagnosis, Enrollment

diagnoses = Diagnosis.objects.all()
count = 0
for d in diagnoses:
    if d.consent_given or d.date_of_consent:
        e, created = Enrollment.objects.get_or_create(patient=d.patient)
        e.consent_given = d.consent_given
        e.date_of_consent = d.date_of_consent
        e.save(update_fields=['consent_given', 'date_of_consent'])
        count += 1

print(f"Migrated {count} enrollments.")
