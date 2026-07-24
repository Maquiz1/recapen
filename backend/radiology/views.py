from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from diagnostics.models import DiagnosticGroup, DiagnosticCategory, DiagnosticTest
from laboratory.forms import CategoryForm, TypeForm

from .forms import RadiologyTestForm

def patient_results_list(request):
    from patients.models import Patient
    # Show patients that have been screened (i.e. tests ordered) or diagnosed
    patients = Patient.objects.filter(status__in=['screened', 'diagnosed', 'enrolled'], is_deleted=False).order_by('-created_at')
    return render(request, 'radiology/patient_results_list.html', {'patients': patients})

def patients_with_results(request):
    from patients.models import Patient
    # Patients who have test results
    patients = Patient.objects.filter(test_results__isnull=False, is_deleted=False).distinct().order_by('-created_at')
    return render(request, 'radiology/patients_results_list.html', {'patients': patients})

def patient_results_detail(request, pk):
    from patients.models import Patient
    patient = get_object_or_404(Patient, pk=pk, is_deleted=False)
    results = patient.test_results.select_related('test').order_by('-performed_date', 'test__test_name')
    return render(request, 'radiology/patient_results_detail.html', {
        'patient': patient,
        'results': results
    })

def pending_orders(request):
    from orders.models import Order
    orders = Order.objects.filter(order_type='radiology', status='pending').order_by('order_date')
    return render(request, 'radiology/pending_orders.html', {'orders': orders})

def fulfill_order(request, pk):
    from orders.models import Order
    from .forms_order import FulfillOrderForm
    order = get_object_or_404(Order, pk=pk, order_type='radiology')
    
    if request.method == 'POST':
        form = FulfillOrderForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.patient = order.patient
            result.test = order.test
            result.order = order
            if request.user.is_authenticated:
                result.created_by = request.user
                result.updated_by = request.user
            result.save()
            
            order.status = 'completed'
            order.save()
            
            messages.success(request, f"Order fulfilled for {order.patient}.")
            return redirect('radiology:pending_orders')
    else:
        form = FulfillOrderForm()
        
    return render(request, 'radiology/fulfill_order.html', {
        'form': form,
        'order': order
    })

def category_list(request):
    categories = DiagnosticGroup.objects.filter(is_deleted=False, department__name='radiology').order_by('name')
    paginator = Paginator(categories, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'radiology/category_list.html', {'categories': page_obj})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            from departments.models import Department
            dept, _ = Department.objects.get_or_create(name='radiology')
            category.department = dept
            if request.user.is_authenticated:
                category.created_by = request.user
                category.updated_by = request.user
            category.save()
            messages.success(request, f"Category '{category.name}' created successfully.")
            return redirect('radiology:category_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm()
    return render(request, 'radiology/category_form.html', {'form': form, 'title': 'Add Radiology Category'})

def category_edit(request, pk):
    category = get_object_or_404(DiagnosticGroup, pk=pk, department__name='radiology')
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f"Category '{category.name}' updated successfully.")
            return redirect('radiology:category_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'radiology/category_form.html', {'form': form, 'title': 'Edit Radiology Category', 'category': category})

def category_delete(request, pk):
    category = get_object_or_404(DiagnosticGroup, pk=pk, is_deleted=False, department__name='radiology')
    
    # Check if category is used in tests
    if DiagnosticTest.objects.filter(diagnostic_group=category, is_deleted=False).exists():
        messages.error(request, f"Cannot delete category '{category.name}' because it contains active tests. Please delete or reassign the tests first.")
        return redirect('radiology:category_list')
        
    category.is_deleted = True
    category.save()
    messages.success(request, f"Category '{category.name}' deleted successfully.")
    return redirect('radiology:category_list')

def category_activate(request, pk):
    category = get_object_or_404(DiagnosticGroup, pk=pk, is_deleted=False, department__name='radiology')
    category.is_active = True
    category.save(update_fields=['is_active'])
    messages.success(request, f"Category '{category.name}' activated successfully.")
    return redirect('radiology:category_list')

def category_deactivate(request, pk):
    category = get_object_or_404(DiagnosticGroup, pk=pk, is_deleted=False, department__name='radiology')
    category.is_active = False
    category.save(update_fields=['is_active'])
    messages.success(request, f"Category '{category.name}' deactivated successfully.")
    return redirect('radiology:category_list')

def type_list(request):
    types = DiagnosticCategory.objects.filter(is_deleted=False, group__department__name='radiology').select_related('group').order_by('group__name', 'name')

    paginator = Paginator(types, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'radiology/type_list.html', {'types': page_obj})

def type_create(request):
    if request.method == 'POST':
        form = TypeForm(request.POST)
        if form.is_valid():
            type_obj = form.save(commit=False)
            if request.user.is_authenticated:
                type_obj.created_by = request.user
                type_obj.updated_by = request.user
            type_obj.save()
            messages.success(request, f"Type '{type_obj.name}' added successfully.")
            return redirect('radiology:type_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TypeForm()
    return render(request, 'radiology/type_form.html', {'form': form, 'title': 'Register New Type'})

def type_edit(request, pk):
    type_obj = get_object_or_404(DiagnosticCategory, pk=pk, is_deleted=False)
    if request.method == 'POST':
        form = TypeForm(request.POST, instance=type_obj)
        if form.is_valid():
            t = form.save(commit=False)
            if request.user.is_authenticated:
                t.updated_by = request.user
            t.save()
            messages.success(request, f"Type '{t.name}' updated successfully.")
            return redirect('radiology:type_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TypeForm(instance=type_obj)
    return render(request, 'radiology/type_form.html', {'form': form, 'title': f'Edit Type: {type_obj.name}'})

def type_delete(request, pk):
    type_obj = get_object_or_404(DiagnosticCategory, pk=pk, is_deleted=False)
    
    # Check if type has any active tests
    if DiagnosticTest.objects.filter(diagnostic_category=type_obj, is_deleted=False).exists():
        messages.error(request, f"Cannot delete '{type_obj.name}' because it contains active tests.")
        return redirect('radiology:type_list')
        
    type_obj.is_deleted = True
    if request.user.is_authenticated:
        type_obj.updated_by = request.user
    type_obj.save()
    messages.success(request, f"Type '{type_obj.name}' deleted successfully.")
    return redirect('radiology:type_list')

def type_activate(request, pk):
    type_obj = get_object_or_404(DiagnosticCategory, pk=pk, is_deleted=False)
    type_obj.is_active = True
    type_obj.save(update_fields=['is_active'])
    messages.success(request, f"Type '{type_obj.name}' activated successfully.")
    return redirect('radiology:type_list')

def type_deactivate(request, pk):
    type_obj = get_object_or_404(DiagnosticCategory, pk=pk, is_deleted=False)
    type_obj.is_active = False
    type_obj.save(update_fields=['is_active'])
    messages.success(request, f"Type '{type_obj.name}' deactivated successfully.")
    return redirect('radiology:type_list')

def test_list(request):
    tests = DiagnosticTest.objects.filter(is_deleted=False, department__name='radiology').select_related('diagnostic_group', 'diagnostic_category').order_by('diagnostic_group__name', 'test_name')
    
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
    
    categories = DiagnosticGroup.objects.filter(is_deleted=False, department__name='radiology').order_by('name')
    types = DiagnosticCategory.objects.filter(is_deleted=False, group__department__name='radiology').order_by('name')
    
    context = {
        'tests': page_obj,
        'total_tests': total_tests,
        'categories': categories,
        'types': types,
        'current_q': q,
        'current_category': category_id,
        'current_type': type_id,
        'current_status': status,
    }
    
    return render(request, 'radiology/test_list.html', context)

def test_create(request):
    if request.method == 'POST':
        form = RadiologyTestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            from departments.models import Department
            dept, _ = Department.objects.get_or_create(name='radiology')
            test.department = dept
            if request.user.is_authenticated:
                test.created_by = request.user
                test.updated_by = request.user
            test.save()
            messages.success(request, f"Radiology test '{test.test_name}' registered successfully.")
            return redirect('radiology:list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RadiologyTestForm()
    return render(request, 'radiology/test_form.html', {'form': form, 'title': 'Register New Test'})

def test_edit(request, pk):
    test = get_object_or_404(DiagnosticTest, pk=pk, is_deleted=False, department__name='radiology')
    if request.method == 'POST':
        form = RadiologyTestForm(request.POST, instance=test)
        if form.is_valid():
            t = form.save(commit=False)
            if request.user.is_authenticated:
                t.updated_by = request.user
            t.save()
            messages.success(request, f"Radiology test '{t.test_name}' updated successfully.")
            return redirect('radiology:list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RadiologyTestForm(instance=test)
    return render(request, 'radiology/test_form.html', {'form': form, 'title': f'Edit Test: {test.test_name}'})

def test_activate(request, pk):
    test = get_object_or_404(DiagnosticTest, pk=pk, is_deleted=False, department__name='radiology')
    test.is_active = True
    test.save()
    messages.success(request, f'Test "{test.test_name}" activated successfully.')
    return redirect('radiology:list')

def test_deactivate(request, pk):
    test = get_object_or_404(DiagnosticTest, pk=pk, is_deleted=False, department__name='radiology')
    test.is_active = False
    test.save()
    messages.warning(request, f'Test "{test.test_name}" deactivated.')
    return redirect('radiology:list')

def test_delete(request, pk):
    test = get_object_or_404(DiagnosticTest, pk=pk, is_deleted=False, department__name='radiology')
    
    from orders.models import Order
    from laboratory.models import PatientTestResult
    
    if PatientTestResult.objects.filter(test=test, is_deleted=False).exists() or Order.objects.filter(test=test, is_deleted=False).exists():
        messages.error(request, f'Cannot delete "{test.test_name}" because it already has associated patient records or orders.')
        return redirect('radiology:list')
        
    test.is_deleted = True
    test.save()
    messages.success(request, f'Test "{test.test_name}" deleted.')
    return redirect('radiology:list')

def test_edit_redirect(request):
    first_test = DiagnosticTest.objects.filter(is_deleted=False, department__name='radiology').first()
    if first_test:
        return redirect('radiology:edit', pk=first_test.pk)
    messages.warning(request, "No radiology tests registered yet. Please create a test first.")
    return redirect('radiology:list')
