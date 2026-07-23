from django.utils import timezone
from datetime import timedelta
from pharmacy.models import InventoryBatch
from medications.models import Medication
from django.db.models import Sum, F, Value
from django.db.models.functions import Coalesce

def pharmacy_notifications(request):
    if not request.user.is_authenticated:
        return {'low_stock_count': 0, 'expiring_soon_count': 0, 'expired_count': 0}

    today = timezone.now().date()
    three_months_from_now = today + timedelta(days=90)

    # 1. Low Stock
    # For each medication, total quantity across all batches <= reorder_level
    medications_with_stock = Medication.objects.annotate(
        total_stock=Sum('batches__quantity_in_stock')
    )
    
    meds_low = medications_with_stock.annotate(
        actual_stock=Coalesce('total_stock', Value(0))
    ).filter(actual_stock__lte=F('reorder_level'), is_active=True).count()

    # 2. Expiring Soon (0 < days to expire <= 90)
    # Exclude those with quantity 0
    expiring_soon = InventoryBatch.objects.filter(
        quantity_in_stock__gt=0,
        expiration_date__gt=today,
        expiration_date__lte=three_months_from_now
    ).count()

    # 3. Expired (expiration_date <= today)
    expired = InventoryBatch.objects.filter(
        quantity_in_stock__gt=0,
        expiration_date__lte=today
    ).count()

    return {
        'low_stock_count': meds_low,
        'expiring_soon_count': expiring_soon,
        'expired_count': expired
    }
