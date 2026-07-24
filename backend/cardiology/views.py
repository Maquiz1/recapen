from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from diagnostics.models import DiagnosticGroup, DiagnosticCategory, DiagnosticTest
from laboratory.forms import GroupForm, CategoryForm

from .forms import CardiologyTestForm

def patient_results_list(request):
    from patients.models import Patient
    # Show patients that have cardiology orders
    patients = Patient.objects.filter(orders__order_category='cardiology', is_deleted=False).distinct().order_by('-created_at')
    return render(request, 'cardiology/patient_results_list.html', {'patients': patients})

def patients_with_results(request):
    from patients.models import Patient
    # Patients who have test results
    patients = Patient.objects.filter(test_results__isnull=False, is_deleted=False).distinct().order_by('-created_at')
    return render(request, 'cardiology/patients_results_list.html', {'patients': patients})

def patient_results_detail(request, pk):
    from patients.models import Patient
    patient = get_object_or_404(Patient, pk=pk, is_deleted=False)
    results = patient.test_results.select_related('test').order_by('-performed_date', 'test__test_name')
    return render(request, 'cardiology/patient_results_detail.html', {
        'patient': patient,
        'results': results
    })

def pending_orders(request):
    from orders.models import Order
    orders = Order.objects.filter(order_category='cardiology', status='pending').order_by('order_date')
    return render(request, 'cardiology/pending_orders.html', {'orders': orders})

def fulfill_order(request, pk):
    from orders.models import Order
    from .forms_order import FulfillOrderForm
    order = get_object_or_404(Order, pk=pk, order_category='cardiology')
    
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
            return redirect('cardiology:pending_orders')
    else:
        form = FulfillOrderForm()
        
    return render(request, 'cardiology/fulfill_order.html', {
        'form': form,
        'order': order
    })

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
