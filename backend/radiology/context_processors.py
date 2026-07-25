from orders.models import Order

def radiology_notifications(request):
    """
    Context processor to inject radiology notifications globally.
    """
    if request.user.is_authenticated:
        pending_rad_count = Order.objects.filter(
            order_type='radiology',
            status__in=['pending', 'in_progress'],
            test__isnull=False
        ).values('patient').distinct().count()
        return {'pending_rad_orders_count': pending_rad_count}
    return {'pending_rad_orders_count': 0}
