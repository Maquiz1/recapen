from django.shortcuts import render, redirect, get_object_or_404

def patient_results_list(request):
    from patients.models import Patient
    # Show patients that have been screened (i.e. tests ordered) or diagnosed
    patients = Patient.objects.filter(status__in=['screened', 'diagnosed', 'enrolled'], is_deleted=False).order_by('-created_at')
    return render(request, 'laboratory/patient_results_list.html', {'patients': patients})

def patients_with_results(request):
    from patients.models import Patient
    # Patients who have test results
    patients = Patient.objects.filter(test_results__isnull=False, is_deleted=False).distinct().order_by('-created_at')
    return render(request, 'laboratory/patients_results_list.html', {'patients': patients})

def patient_results_detail(request, pk):
    from patients.models import Patient
    from collections import defaultdict
    import datetime
    from django.utils import timezone
    
    patient = get_object_or_404(Patient, pk=pk, is_deleted=False)
    results = patient.test_results.select_related('test').order_by('-performed_date', 'test__name')
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    date_type = request.GET.get('date_type', 'visit_date')
    
    # Base queryset with select_related for orders/encounters
    results = patient.test_results.select_related('test', 'order', 'order__encounter')
    
    # Map date_type to the respective query field
    date_field_map = {
        'visit_date': 'order__encounter__start_time__date',
        'request_date': 'order__order_date__date',
        'result_date': 'performed_date__date'
    }
    
    filter_field = date_field_map.get(date_type, 'order__encounter__start_time__date')
    
    if start_date:
        try:
            parsed_start = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            results = results.filter(**{f"{filter_field}__gte": parsed_start})
        except ValueError:
            pass

    if end_date:
        try:
            parsed_end = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
            results = results.filter(**{f"{filter_field}__lte": parsed_end})
        except ValueError:
            pass
            
    # Apply ordering to newest first, based on the selected date_type
    order_field_map = {
        'visit_date': '-order__encounter__start_time',
        'request_date': '-order__order_date',
        'result_date': '-performed_date'
    }
    order_field = order_field_map.get(date_type, '-order__encounter__start_time')
    results = results.order_by(order_field, 'test__name')
            
    # Group by the dynamically selected Date, then by Category
    grouped_results = defaultdict(lambda: defaultdict(list))
    for res in results:
        # Resolve the actual date value for grouping based on date_type
        if date_type == 'visit_date' and res.order and res.order.encounter:
            group_date = res.order.encounter.start_time
        elif date_type == 'request_date' and res.order:
            group_date = res.order.order_date
        else:
            group_date = res.performed_date
            
        date_key = group_date.strftime("%d %b %Y") if group_date else "Unknown Date"
        
        cat_key = res.test.laboratory_category.name if res.test.laboratory_category else 'Uncategorized'
        grouped_results[date_key][cat_key].append(res)
        
    # Convert to normal dicts
    grouped_results = {d: dict(cats) for d, cats in grouped_results.items()}

    # Determine Display Label for the Accordion based on date_type
    date_type_labels = {
        'visit_date': 'Visit Date',
        'request_date': 'Request Date',
        'result_date': 'Result Date'
    }
    date_type_label = date_type_labels.get(date_type, 'Visit Date')

    return render(request, 'laboratory/patient_results_detail.html', {
        'patient': patient,
        'grouped_results': grouped_results,
        'start_date': start_date,
        'end_date': end_date,
        'date_type': date_type,
        'date_type_label': date_type_label
    })
