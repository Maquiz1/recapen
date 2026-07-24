from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from orders.models import Order
from datetime import datetime

@login_required
def lab_dashboard(request):
    """
    Shows a list of patients who have pending or in_progress lab orders.
    """
    # Base query for lab orders that are not completed or cancelled
    query = Q(order_type='lab', test__isnull=False)
    
    # Filter by status
    status_filter = request.GET.get('status', 'all')
    if status_filter == 'pending':
        query &= Q(status='pending')
    elif status_filter == 'in_progress':
        query &= Q(status='in_progress')
    else:
        query &= Q(status__in=['pending', 'in_progress'])
        
    # Filter by date range
    start_date_str = request.GET.get('start_date', '')
    end_date_str = request.GET.get('end_date', '')
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            query &= Q(order_date__date__gte=start_date)
        except ValueError:
            pass
    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            query &= Q(order_date__date__lte=end_date)
        except ValueError:
            pass
            
    # Filter by search (patient name or MRN)
    search_query = request.GET.get('search', '').strip()
    if search_query:
        query &= (
            Q(patient__first_name__icontains=search_query) |
            Q(patient__last_name__icontains=search_query) |
            Q(patient__mrn__icontains=search_query)
        )

    pending_orders = Order.objects.filter(query).select_related('patient').order_by('patient_id', 'order_date')

    patients_dict = {}
    for order in pending_orders:
        p_id = order.patient.id
        if p_id not in patients_dict:
            patients_dict[p_id] = {
                'patient': order.patient,
                'order_count': 0,
                'oldest_order_date': order.order_date,
                'has_stat': False,
                'has_urgent': False,
                'status': 'pending'
            }
        
        patients_dict[p_id]['order_count'] += 1
        
        if order.urgency == 'stat':
            patients_dict[p_id]['has_stat'] = True
        elif order.urgency == 'urgent':
            patients_dict[p_id]['has_urgent'] = True
            
        if order.status == 'in_progress':
            patients_dict[p_id]['status'] = 'in_progress'

    # Convert to list and sort by urgency (STAT first), then date DESC (newest first)
    patient_list = list(patients_dict.values())
    patient_list.sort(key=lambda x: (
        0 if x['has_stat'] else (1 if x['has_urgent'] else 2),
        -x['oldest_order_date'].timestamp()
    ))

    # Pagination: 10 records per page
    paginator = Paginator(patient_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search': search_query,
        'start_date': start_date_str,
        'end_date': end_date_str,
        'status': status_filter,
    }
    return render(request, 'laboratory/dashboard.html', context)
