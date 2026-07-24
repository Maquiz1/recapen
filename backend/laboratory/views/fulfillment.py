from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from orders.models import Order
from laboratory.models.results import PatientTestResult
from laboratory.models.tests import LaboratoryTest

@login_required
def fulfill_lab_order(request, patient_id):
    from orders.models import Order
    from patients.models import Patient
    from laboratory.models import PatientTestResult

    patient = get_object_or_404(Patient, pk=patient_id)
    
    # Fetch all pending lab orders for this patient
    pending_orders = list(Order.objects.filter(
        patient=patient,
        order_type='lab',
        status__in=['pending', 'in_progress'],
        test__isnull=False
    ).select_related('test', 'test__laboratory_category', 'test__laboratory_type', 'ordering_doctor'))

    if not pending_orders:
        messages.info(request, f"No pending laboratory orders found for {patient}.")
        return redirect('laboratory:lab_dashboard')
        
    # Mark them all as in_progress
    Order.objects.filter(id__in=[o.id for o in pending_orders], status='pending').update(status='in_progress')

    # Gather all sub-tests for all ordered panels/tests
    all_tests_to_fulfill = []
    order_map = {} # Map test.id -> order object (so we know which order to complete later)
    
    for order in pending_orders:
        if order.test.is_panel:
            sub_tests = order.test.sub_tests.filter(is_active=True, is_deleted=False)
            for sub_test in sub_tests:
                all_tests_to_fulfill.append(sub_test)
                order_map[sub_test.id] = order
        else:
            all_tests_to_fulfill.append(order.test)
            order_map[order.test.id] = order
            
    # Group tests by Category and Type for the template
    grouped_tests = {}
    for test in all_tests_to_fulfill:
        cat_name = test.laboratory_category.name if test.laboratory_category else "Uncategorized"
        type_name = test.laboratory_type.name if test.laboratory_type else "General"
        
        if cat_name not in grouped_tests:
            grouped_tests[cat_name] = {}
        if type_name not in grouped_tests[cat_name]:
            grouped_tests[cat_name][type_name] = []
            
        grouped_tests[cat_name][type_name].append(test)

    if request.method == 'POST':
        completed_orders = set()
        
        for test in all_tests_to_fulfill:
            val_str = request.POST.get(f'result_{test.id}')
            if val_str and val_str.strip():
                notes = request.POST.get(f'notes_{test.id}', '')
                
                # Determine flag
                flag = 'NORMAL'
                try:
                    val = float(val_str)
                    if test.range_min:
                        try:
                            min_val = float(test.range_min)
                            if val < min_val:
                                flag = 'LOW'
                        except ValueError:
                            pass
                            
                    if test.range_max:
                        try:
                            max_val = float(test.range_max)
                            if val > max_val:
                                flag = 'HIGH'
                        except ValueError:
                            pass
                except ValueError:
                    # If it's a string result (like 'Positive'), we just store it
                    pass
                    
                # Create the result
                PatientTestResult.objects.create(
                    patient=patient,
                    order=order_map[test.id], # link to the specific order
                    test=test,
                    result_value=val_str,
                    flag=flag,
                    notes=notes,
                    entered_by=request.user
                )
                
                if test.id in order_map:
                    completed_orders.add(order_map[test.id])
                    
        # Update orders to completed
        for order in completed_orders:
            order.status = 'completed'
            order.save()
            
        messages.success(request, f"Results successfully entered for {patient}.")
        return redirect('laboratory:lab_dashboard')
        
    has_stat = any(o.urgency == 'stat' for o in pending_orders)
    has_urgent = any(o.urgency == 'urgent' for o in pending_orders)

    category_counts = {}
    for cat_name, types in grouped_tests.items():
        category_counts[cat_name] = sum(len(tests) for tests in types.values())

    context = {
        'patient': patient,
        'grouped_tests': grouped_tests,
        'category_counts': category_counts,
        'highest_urgency': 'stat' if has_stat else ('urgent' if has_urgent else 'routine'),
        'first_doctor': pending_orders[0].ordering_doctor if pending_orders else None
    }
    return render(request, 'laboratory/fulfillment.html', context)

@login_required
def edit_lab_results(request, patient_id, date_type, date_string):
    from patients.models import Patient
    from laboratory.models.results import PatientTestResult
    from collections import defaultdict
    import datetime
    
    patient = get_object_or_404(Patient, pk=patient_id)
    
    # Base queryset for existing results
    results = PatientTestResult.objects.filter(patient=patient).select_related('test', 'test__laboratory_category', 'test__laboratory_type', 'order', 'order__encounter', 'order__ordering_doctor')
    
    # Filter down to the specific date string
    try:
        parsed_date = datetime.datetime.strptime(date_string, '%d %b %Y').date()
    except ValueError:
        messages.error(request, "Invalid date format.")
        return redirect('laboratory:patient_detail', pk=patient_id)
        
    date_field_map = {
        'visit_date': 'order__encounter__start_time__date',
        'request_date': 'order__order_date__date',
        'result_date': 'performed_date__date'
    }
    filter_field = date_field_map.get(date_type, 'order__encounter__start_time__date')
    results = results.filter(**{filter_field: parsed_date})
    
    if not results.exists():
        messages.warning(request, "No results found for the specified date.")
        return redirect('laboratory:patient_detail', pk=patient_id)
        
    if request.method == 'POST':
        for res in results:
            val_str = request.POST.get(f'result_{res.id}')
            if val_str and val_str.strip():
                notes = request.POST.get(f'notes_{res.id}', '')
                
                # Determine flag
                flag = 'NORMAL'
                try:
                    val = float(val_str)
                    if res.test.range_min:
                        try:
                            min_val = float(res.test.range_min)
                            if val < min_val:
                                flag = 'LOW'
                        except ValueError:
                            pass
                            
                    if res.test.range_max:
                        try:
                            max_val = float(res.test.range_max)
                            if val > max_val:
                                flag = 'HIGH'
                        except ValueError:
                            pass
                except ValueError:
                    pass
                    
                # Update existing record
                res.result_value = val_str
                res.flag = flag
                res.notes = notes
                res.save()
                
        messages.success(request, f"Results successfully updated for {patient}.")
        return redirect('laboratory:patient_detail', pk=patient_id)
        
    # Group results by Category and Type for the template
    grouped_results = defaultdict(lambda: defaultdict(list))
    for res in results:
        cat = res.test.laboratory_category.name if res.test.laboratory_category else "Uncategorized"
        typ = res.test.laboratory_type.name if res.test.laboratory_type else "General"
        grouped_results[cat][typ].append(res)
        
    grouped_results = {k: dict(v) for k, v in grouped_results.items()}
    
    category_counts = {}
    for cat_name, types in grouped_results.items():
        pending_count = 0
        for tests in types.values():
            for res in tests:
                if not res.result_value:
                    pending_count += 1
        category_counts[cat_name] = pending_count
    
    first_order = results.first().order
    first_doctor = first_order.ordering_doctor if first_order else None
    
    context = {
        'patient': patient,
        'grouped_results': grouped_results,
        'category_counts': category_counts,
        'date_string': date_string,
        'date_type_label': date_type.replace('_', ' ').title(),
        'first_doctor': first_doctor
    }
    return render(request, 'laboratory/edit_results.html', context)

