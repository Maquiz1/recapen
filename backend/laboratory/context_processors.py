from orders.models import Order

def laboratory_notifications(request):
    """
    Context processor to inject laboratory notifications globally.
    """
    if request.user.is_authenticated:
        pending_lab_count = Order.objects.filter(
            order_type='lab',
            status__in=['pending', 'in_progress'],
            test__isnull=False
        ).values('patient').distinct().count()
        return {'pending_lab_orders_count': pending_lab_count}
    return {'pending_lab_orders_count': 0}
