from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from diagnostics.models import DiagnosticGroup, DiagnosticCategory, DiagnosticTest
from laboratory.forms import LabTestForm

def test_list(request):
    tests = DiagnosticTest.objects.filter(is_deleted=False, department__name='laboratory').select_related('diagnostic_group', 'diagnostic_category').order_by('diagnostic_group__name', 'test_name')
    
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
    
    categories = DiagnosticGroup.objects.filter(is_deleted=False, department__name='laboratory').order_by('name')
    types = DiagnosticCategory.objects.filter(is_deleted=False, group__department__name='laboratory').order_by('name')
    
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
    
    return render(request, 'laboratory/test_list.html', context)

def test_create(request):
    if request.method == 'POST':
        form = LabTestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            from departments.models import Department
            dept, _ = Department.objects.get_or_create(name='laboratory')
            test.department = dept
            if request.user.is_authenticated:
                test.created_by = request.user
                test.updated_by = request.user
            test.save()
            messages.success(request, f"Laboratory test '{test.test_name}' registered successfully.")
            return redirect('laboratory:list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LabTestForm()
    return render(request, 'laboratory/test_form.html', {'form': form, 'title': 'Register New Test'})

def test_edit(request, pk):
    test = get_object_or_404(DiagnosticTest, pk=pk, is_deleted=False, department__name='laboratory')
    if request.method == 'POST':
        form = LabTestForm(request.POST, instance=test)
        if form.is_valid():
            t = form.save(commit=False)
            if request.user.is_authenticated:
                t.updated_by = request.user
            t.save()
            messages.success(request, f"Laboratory test '{t.test_name}' updated successfully.")
            return redirect('laboratory:list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LabTestForm(instance=test)
    return render(request, 'laboratory/test_form.html', {'form': form, 'title': f'Edit Test: {test.test_name}'})

def test_activate(request, pk):
    test = get_object_or_404(DiagnosticTest, pk=pk, is_deleted=False, department__name='laboratory')
    test.is_active = True
    test.save()
    messages.success(request, f'Test "{test.test_name}" activated successfully.')
    return redirect('laboratory:list')

def test_deactivate(request, pk):
    test = get_object_or_404(DiagnosticTest, pk=pk, is_deleted=False, department__name='laboratory')
    test.is_active = False
    test.save()
    messages.warning(request, f'Test "{test.test_name}" deactivated.')
    return redirect('laboratory:list')

def test_delete(request, pk):
    test = get_object_or_404(DiagnosticTest, pk=pk, is_deleted=False, department__name='laboratory')
    
    from orders.models import Order
    from laboratory.models import PatientTestResult
    
    if PatientTestResult.objects.filter(test=test, is_deleted=False).exists() or Order.objects.filter(test=test, is_deleted=False).exists():
        messages.error(request, f'Cannot delete "{test.test_name}" because it already has associated patient records or orders.')
        return redirect('laboratory:list')
        
    test.is_deleted = True
    test.save()
    messages.success(request, f'Test "{test.test_name}" deleted.')
    return redirect('laboratory:list')

def test_edit_redirect(request):
    first_test = DiagnosticTest.objects.filter(is_deleted=False, department__name='laboratory').first()
    if first_test:
        return redirect('laboratory:edit', pk=first_test.pk)
    messages.warning(request, "No lab tests registered yet. Please create a lab test first.")
    return redirect('laboratory:list')
