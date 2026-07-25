from datetime import datetime
from django.db.models import Q
from orders.models import Order
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from diagnostics.models import DiagnosticGroup, DiagnosticCategory, DiagnosticTest
from laboratory.forms import GroupForm, CategoryForm

from .forms import CardiologyTestForm

def patients_with_results(request):
    from patients.models import Patient
    # Patients who have test results
    patients = Patient.objects.filter(test_results__isnull=False, is_deleted=False).distinct().order_by('-created_at')
    return render(request, 'cardiology/patients_results_list.html', {'patients': patients})

def patient_results_detail(request, pk):
    from patients.models import Patient
    from collections import defaultdict
    from datetime import datetime
    
    patient = get_object_or_404(Patient, pk=pk, is_deleted=False)
    results = patient.test_results.select_related('test').filter(order__order_type='cardiology').order_by('-performed_date', 'test__test_name')
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    date_type = request.GET.get('date_type', 'visit_date')
    
    if start_date:
        try:
            parsed_start = datetime.strptime(start_date, '%d-%b-%Y').date()
            filter_field = 'performed_date__date'
            if date_type == 'visit_date':
                filter_field = 'order__encounter__start_time__date'
            elif date_type == 'request_date':
                filter_field = 'order__order_date'
            results = results.filter(**{f"{filter_field}__gte": parsed_start})
        except ValueError:
            pass
            
    if end_date:
        try:
            parsed_end = datetime.strptime(end_date, '%d-%b-%Y').date()
            filter_field = 'performed_date__date'
            if date_type == 'visit_date':
                filter_field = 'order__encounter__start_time__date'
            elif date_type == 'request_date':
                filter_field = 'order__order_date'
            results = results.filter(**{f"{filter_field}__lte": parsed_end})
        except ValueError:
            pass
            
    order_field_map = {
        'visit_date': '-order__encounter__start_time',
        'request_date': '-order__order_date',
        'result_date': '-performed_date'
    }
    order_field = order_field_map.get(date_type, '-order__encounter__start_time')
    results = results.order_by(order_field, 'test__test_name')
            
    grouped_results = defaultdict(lambda: defaultdict(list))
    for res in results:
        if date_type == 'visit_date' and res.order and res.order.encounter:
            group_date = res.order.encounter.start_time
        elif date_type == 'request_date' and res.order:
            group_date = res.order.order_date
        else:
            group_date = res.performed_date
            
        date_key = group_date.strftime("%d %b %Y") if group_date else "Unknown Date"
        cat_key = res.test.diagnostic_category.name if res.test.diagnostic_category else 'Uncategorized'
        grouped_results[date_key][cat_key].append(res)
        
    grouped_results = {d: dict(sorted(cats.items())) for d, cats in grouped_results.items()}

    date_type_labels = {
        'visit_date': 'Visit Date',
        'request_date': 'Request Date',
        'result_date': 'Result Date'
    }
    
    return render(request, 'cardiology/patient_results_detail.html', {
        'patient': patient,
        'grouped_results': grouped_results,
        'date_type': date_type,
        'start_date': start_date,
        'end_date': end_date,
        'date_type_label': date_type_labels.get(date_type, 'Visit Date')
    })

@login_required
def pending_orders(request):
    """
    Shows a list of patients who have pending or in_progress lab orders.
    """
    from django.db.models import Q
    from orders.models import Order
    from datetime import datetime
    from django.core.paginator import Paginator

    # Base query for lab orders that are not completed or cancelled
    query = Q(order_type='cardiology', test__isnull=False)
    
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
    return render(request, 'cardiology/pending_orders.html', context)


def fulfill_order(request, pk):
    from orders.models import Order
    from patients.models import Patient
    from laboratory.models.results import PatientTestResult
    from django.contrib import messages
    from django.shortcuts import render, get_object_or_404, redirect

    patient_id = pk
    patient = get_object_or_404(Patient, pk=patient_id)
    
    # Fetch all pending cardiology orders for this patient
    pending_orders = list(Order.objects.filter(
        patient=patient,
        order_type='cardiology',
        status__in=['pending', 'in_progress'],
        test__isnull=False
    ).select_related('test', 'test__diagnostic_group', 'test__diagnostic_category', 'ordering_doctor'))

    if not pending_orders:
        messages.info(request, f"No pending cardiology orders found for {patient}.")
        return redirect('cardiology:pending_orders')
        
    # Mark them all as in_progress
    Order.objects.filter(id__in=[o.id for o in pending_orders], status='pending').update(status='in_progress')

    all_tests_to_fulfill = []
    order_map = {} 
    
    for order in pending_orders:
        all_tests_to_fulfill.append(order.test)
        order_map[order.test.id] = order
            
    # Group tests by Category and Type for the template
    grouped_tests = {}
    for test in all_tests_to_fulfill:
        cat_name = test.diagnostic_group.name if test.diagnostic_group else "Uncategorized"
        group_name = test.diagnostic_category.name if test.diagnostic_category else "General"
        
        if cat_name not in grouped_tests:
            grouped_tests[cat_name] = {}
        if group_name not in grouped_tests[cat_name]:
            grouped_tests[cat_name][group_name] = []
            
        grouped_tests[cat_name][group_name].append(test)

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
                            if val < float(test.range_min):
                                flag = 'LOW'
                        except ValueError:
                            pass
                            
                    if test.range_max:
                        try:
                            if val > float(test.range_max):
                                flag = 'HIGH'
                        except ValueError:
                            pass
                except ValueError:
                    pass
                    
                PatientTestResult.objects.create(
                    patient=patient,
                    order=order_map[test.id],
                    test=test,
                    result_value=val_str,
                    flag=flag,
                    notes=notes,
                    entered_by=request.user if request.user.is_authenticated else None
                )
                
                if test.id in order_map:
                    completed_orders.add(order_map[test.id])
                    
        for order in completed_orders:
            order.status = 'completed'
            order.save()
            
        messages.success(request, f"Results successfully entered for {patient}.")
        return redirect('cardiology:pending_orders')
        
    has_stat = any(o.urgency == 'stat' for o in pending_orders)
    has_urgent = any(o.urgency == 'urgent' for o in pending_orders)

    category_counts = {}
    for cat_name, groups in grouped_tests.items():
        category_counts[cat_name] = sum(len(tests) for tests in groups.values())

    context = {
        'patient': patient,
        'grouped_tests': grouped_tests,
        'category_counts': category_counts,
        'highest_urgency': 'stat' if has_stat else ('urgent' if has_urgent else 'routine'),
        'first_doctor': pending_orders[0].ordering_doctor if pending_orders else None
    }
    return render(request, 'cardiology/fulfillment.html', context)

def group_list(request):
    groups = DiagnosticGroup.objects.filter(is_deleted=False, department__name='cardiology').order_by('name')
    paginator = Paginator(groups, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'cardiology/group_list.html', {'groups': page_obj})

def group_create(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            from departments.models import Department
            dept, _ = Department.objects.get_or_create(name='cardiology')
            group.department = dept
            if request.user.is_authenticated:
                group.created_by = request.user
                group.updated_by = request.user
            group.save()
            messages.success(request, f"Group '{group.name}' created successfully.")
            return redirect('cardiology:group_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = GroupForm()
    return render(request, 'cardiology/category_form.html', {'form': form, 'title': 'Add Cardiology Category'})

def group_edit(request, pk):
    category = get_object_or_404(DiagnosticGroup, pk=pk, department__name='cardiology')
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f"Group '{group.name}' updated successfully.")
            return redirect('cardiology:group_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = GroupForm(instance=category)
    return render(request, 'cardiology/category_form.html', {'form': form, 'title': 'Edit Cardiology Category', 'category': category})

def group_delete(request, pk):
    category = get_object_or_404(DiagnosticGroup, pk=pk, is_deleted=False, department__name='cardiology')
    
    # Check if category is used in tests
    if DiagnosticTest.objects.filter(diagnostic_group=category, is_deleted=False).exists():
        messages.error(request, f"Cannot delete category '{group.name}' because it contains active tests. Please delete or reassign the tests first.")
        return redirect('cardiology:group_list')
        
    group.is_deleted = True
    group.save()
    messages.success(request, f"Group '{group.name}' deleted successfully.")
    return redirect('cardiology:group_list')

def group_activate(request, pk):
    category = get_object_or_404(DiagnosticGroup, pk=pk, is_deleted=False, department__name='cardiology')
    group.is_active = True
    group.save(update_fields=['is_active'])
    messages.success(request, f"Group '{group.name}' activated successfully.")
    return redirect('cardiology:group_list')

def group_deactivate(request, pk):
    category = get_object_or_404(DiagnosticGroup, pk=pk, is_deleted=False, department__name='cardiology')
    group.is_active = False
    group.save(update_fields=['is_active'])
    messages.success(request, f"Group '{group.name}' deactivated successfully.")
    return redirect('cardiology:group_list')

def category_list(request):
    categories = DiagnosticCategory.objects.filter(is_deleted=False, group__department__name='cardiology').select_related('group').order_by('group__name', 'name')

    paginator = Paginator(categories, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'cardiology/category_list.html', {'categories': page_obj})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            type_obj = form.save(commit=False)
            if request.user.is_authenticated:
                category.created_by = request.user
                category.updated_by = request.user
            category.save()
            messages.success(request, f"Category '{category.name}' added successfully.")
            return redirect('cardiology:category_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm()
    return render(request, 'cardiology/type_form.html', {'form': form, 'title': 'Register New Type'})

def category_edit(request, pk):
    type_obj = get_object_or_404(DiagnosticCategory, pk=pk, is_deleted=False)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=type_obj)
        if form.is_valid():
            t = form.save(commit=False)
            if request.user.is_authenticated:
                t.updated_by = request.user
            t.save()
            messages.success(request, f"Category '{t.name}' updated successfully.")
            return redirect('cardiology:category_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm(instance=type_obj)
    return render(request, 'cardiology/type_form.html', {'form': form, 'title': f'Edit Type: {category.name}'})

def category_delete(request, pk):
    type_obj = get_object_or_404(DiagnosticCategory, pk=pk, is_deleted=False)
    
    # Check if type has any active tests
    if DiagnosticTest.objects.filter(diagnostic_group=type_obj, is_deleted=False).exists():
        messages.error(request, f"Cannot delete '{category.name}' because it contains active tests.")
        return redirect('cardiology:category_list')
        
    category.is_deleted = True
    if request.user.is_authenticated:
        category.updated_by = request.user
    category.save()
    messages.success(request, f"Category '{category.name}' deleted successfully.")
    return redirect('cardiology:category_list')

def category_activate(request, pk):
    type_obj = get_object_or_404(DiagnosticCategory, pk=pk, is_deleted=False)
    category.is_active = True
    category.save(update_fields=['is_active'])
    messages.success(request, f"Category '{category.name}' activated successfully.")
    return redirect('cardiology:category_list')

def category_deactivate(request, pk):
    type_obj = get_object_or_404(DiagnosticCategory, pk=pk, is_deleted=False)
    category.is_active = False
    category.save(update_fields=['is_active'])
    messages.success(request, f"Category '{category.name}' deactivated successfully.")
    return redirect('cardiology:category_list')

def test_list(request):
    tests = DiagnosticTest.objects.filter(is_deleted=False, department__name='cardiology').select_related('diagnostic_group', 'diagnostic_category').order_by('diagnostic_group__name', 'test_name')
    
    # Filtering
    q = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '')
    type_id = request.GET.get('type', '')
    status = request.GET.get('status', '')
    
    if q:
        tests = tests.filter(test_name__icontains=q)
    if category_id:
        tests = tests.filter(diagnostic_group_id=category_id)
    if type_id:
        tests = tests.filter(diagnostic_category_id=type_id)
    if status == 'active':
        tests = tests.filter(is_active=True)
    elif status == 'inactive':
        tests = tests.filter(is_active=False)
        
    tests = tests.order_by('diagnostic_group__name', 'diagnostic_category__name', 'test_name')
    total_tests = tests.count()
    
    paginator = Paginator(tests, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    groups = DiagnosticGroup.objects.filter(is_deleted=False, department__name='cardiology').order_by('name')
    categories = DiagnosticCategory.objects.filter(is_deleted=False, group__department__name='cardiology').order_by('name')
    
    context = {
        'tests': page_obj,
        'total_tests': total_tests,
        'groups': groups,
        'categories': categories,
        'current_q': q,
        'current_category': category_id,
        'current_type': type_id,
        'current_status': status,
    }
    
    return render(request, 'cardiology/test_list.html', context)

def test_create(request):
    if request.method == 'POST':
        form = CardiologyTestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            from departments.models import Department
            dept, _ = Department.objects.get_or_create(name='cardiology')
            test.department = dept
            if request.user.is_authenticated:
                test.created_by = request.user
                test.updated_by = request.user
            test.save()
            messages.success(request, f"Cardiology test '{test.test_name}' registered successfully.")
            return redirect('cardiology:list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CardiologyTestForm()
    return render(request, 'cardiology/test_form.html', {'form': form, 'title': 'Register New Test'})

def test_edit(request, pk):
    test = get_object_or_404(DiagnosticTest, pk=pk, is_deleted=False, department__name='cardiology')
    if request.method == 'POST':
        form = CardiologyTestForm(request.POST, instance=test)
        if form.is_valid():
            t = form.save(commit=False)
            if request.user.is_authenticated:
                t.updated_by = request.user
            t.save()
            messages.success(request, f"Cardiology test '{t.test_name}' updated successfully.")
            return redirect('cardiology:list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CardiologyTestForm(instance=test)
    return render(request, 'cardiology/test_form.html', {'form': form, 'title': f'Edit Test: {test.test_name}'})

def test_activate(request, pk):
    test = get_object_or_404(DiagnosticTest, pk=pk, is_deleted=False, department__name='cardiology')
    test.is_active = True
    test.save()
    messages.success(request, f'Test "{test.test_name}" activated successfully.')
    return redirect('cardiology:list')

def test_deactivate(request, pk):
    test = get_object_or_404(DiagnosticTest, pk=pk, is_deleted=False, department__name='cardiology')
    test.is_active = False
    test.save()
    messages.warning(request, f'Test "{test.test_name}" deactivated.')
    return redirect('cardiology:list')

def test_delete(request, pk):
    test = get_object_or_404(DiagnosticTest, pk=pk, is_deleted=False, department__name='cardiology')
    
    from orders.models import Order
    from laboratory.models import PatientTestResult
    
    if PatientTestResult.objects.filter(test=test, is_deleted=False).exists() or Order.objects.filter(test=test, is_deleted=False).exists():
        messages.error(request, f'Cannot delete "{test.test_name}" because it already has associated patient records or orders.')
        return redirect('cardiology:list')
        
    test.is_deleted = True
    test.save()
    messages.success(request, f'Test "{test.test_name}" deleted.')
    return redirect('cardiology:list')

def test_edit_redirect(request):
    first_test = DiagnosticTest.objects.filter(is_deleted=False, department__name='cardiology').first()
    if first_test:
        return redirect('cardiology:edit', pk=first_test.pk)
    messages.warning(request, "No cardiology tests registered yet. Please create a test first.")
    return redirect('cardiology:list')
