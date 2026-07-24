import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from laboratory.models import LaboratoryTest

tests = LaboratoryTest.objects.all()
for test in tests:
    if test.reference_range:
        parts = test.reference_range.split('-')
        if len(parts) == 2:
            test.range_min = parts[0].strip()
            test.range_max = parts[1].strip()
            test.save()
            print(f"Updated {test.name}: min={test.range_min}, max={test.range_max}")
        else:
            test.range_min = test.reference_range
            test.save()
            print(f"Updated {test.name}: min={test.range_min}")
