import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recapen.settings")
django.setup()
from orders.models import Order
print([(o.id, o.order_type, o.status, o.test.test_name if o.test else None) for o in Order.objects.all()])
