from orders.models import Order

def cardiology_notifications(request):
    """
    Context processor to inject cardiology notifications globally.
    """
    if request.user.is_authenticated:
        pending_cardio_count = Order.objects.filter(
            order_type='cardiology',
            status__in=['pending', 'in_progress'],
            test__isnull=False
        ).values('patient').distinct().count()
        return {'pending_cardio_orders_count': pending_cardio_count}
    return {'pending_cardio_orders_count': 0}
