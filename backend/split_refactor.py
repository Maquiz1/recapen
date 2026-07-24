import os

base_dir = '/home/maquiz/Documents/FINAL_PROJECTS/recapen/backend/laboratory'

def split_models():
    # Read the existing tests.py (which has everything)
    with open(os.path.join(base_dir, 'models', 'tests.py'), 'r') as f:
        content = f.read()

    categories_code = """from django.db import models
from core.models import AuditableModel

class LaboratoryCategory(AuditableModel):
    name = models.CharField(max_length=150, unique=True, help_text="e.g. Haematology, Clinical Chemistry")
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Laboratory Categories"

    def __str__(self):
        return self.name

class LaboratoryType(AuditableModel):
    category = models.ForeignKey(LaboratoryCategory, on_delete=models.CASCADE, related_name='types')
    name = models.CharField(max_length=150, help_text="e.g. Renal Function Test")
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Laboratory Types"
        unique_together = ('category', 'name')

    def __str__(self):
        return f"{self.category.name} - {self.name}"
"""

    tests_code = """from django.db import models
from core.models import AuditableModel
from .categories import LaboratoryCategory, LaboratoryType

class LaboratoryTest(AuditableModel):
    name = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=50, unique=True, help_text="Unique slug e.g. hba1c, ecg, echo")
    # New LMS Fields
    laboratory_category = models.ForeignKey(LaboratoryCategory, on_delete=models.SET_NULL, blank=True, null=True, related_name='tests', help_text="Specific laboratory category")
    laboratory_type = models.ForeignKey(LaboratoryType, on_delete=models.SET_NULL, blank=True, null=True, related_name='tests', help_text="Specific laboratory type")
    range_min = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. '12.5', '0', 'Negative'")
    range_max = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. '18.0', '0', 'N/A'")
    units = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. 'g/dl', 'Reactive'")
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Cost of the test")
    
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    # Panel features
    is_panel = models.BooleanField(default=False, help_text="If True, this is a group of tests (e.g. BMP).")
    parent_panel = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_tests', help_text="If this test is part of a panel, link it here.")
    def __str__(self):
        return self.name
"""

    results_code = """from django.db import models
from core.models import AuditableModel
from .tests import LaboratoryTest

class PatientTestResult(AuditableModel):
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='test_results')
    test = models.ForeignKey(LaboratoryTest, on_delete=models.CASCADE)
    order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True, blank=True, related_name='results')
    result_value = models.CharField(max_length=255, blank=True, null=True, help_text="Entered lab result value")
    performed_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.test.name} for {self.patient}: {self.result_value}"
"""

    with open(os.path.join(base_dir, 'models', 'categories.py'), 'w') as f:
        f.write(categories_code)
    
    with open(os.path.join(base_dir, 'models', 'tests.py'), 'w') as f:
        f.write(tests_code)
        
    with open(os.path.join(base_dir, 'models', 'results.py'), 'w') as f:
        f.write(results_code)

    with open(os.path.join(base_dir, 'models', '__init__.py'), 'w') as f:
        f.write("from .categories import *\nfrom .tests import *\nfrom .results import *\n")


def split_views():
    # Write tests views
    tests_views = """from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from laboratory.models import LaboratoryTest
from laboratory.forms import LabTestForm
from django.core.paginator import Paginator

def test_list(request):
    tests = LaboratoryTest.objects.filter(is_deleted=False).order_by('laboratory_category__name', 'laboratory_type__name', 'name')
    paginator = Paginator(tests, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'laboratory/test_list.html', {'tests': page_obj})

def test_create(request):
    if request.method == 'POST':
        form = LabTestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            if request.user.is_authenticated:
                test.created_by = request.user
                test.updated_by = request.user
            test.save()
            messages.success(request, f"Laboratory test '{test.name}' registered successfully.")
            return redirect('laboratory:list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LabTestForm()
    return render(request, 'laboratory/test_form.html', {'form': form, 'title': 'Register New Test'})

def test_edit(request, pk):
    test = get_object_or_404(LaboratoryTest, pk=pk, is_deleted=False)
    if request.method == 'POST':
        form = LabTestForm(request.POST, instance=test)
        if form.is_valid():
            t = form.save(commit=False)
            if request.user.is_authenticated:
                t.updated_by = request.user
            t.save()
            messages.success(request, f"Laboratory test '{t.name}' updated successfully.")
            return redirect('laboratory:list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LabTestForm(instance=test)
    return render(request, 'laboratory/test_form.html', {'form': form, 'title': f'Edit Test: {test.name}'})

def test_activate(request, pk):
    test = get_object_or_404(LaboratoryTest, pk=pk, is_deleted=False)
    test.is_active = True
    test.save()
    messages.success(request, f'Test "{test.name}" activated successfully.')
    return redirect('laboratory:list')

def test_deactivate(request, pk):
    test = get_object_or_404(LaboratoryTest, pk=pk, is_deleted=False)
    test.is_active = False
    test.save()
    messages.warning(request, f'Test "{test.name}" deactivated.')
    return redirect('laboratory:list')

def test_delete(request, pk):
    test = get_object_or_404(LaboratoryTest, pk=pk, is_deleted=False)
    test.is_deleted = True
    test.save()
    messages.error(request, f'Test "{test.name}" deleted.')
    return redirect('laboratory:list')

def test_edit_redirect(request):
    first_test = LaboratoryTest.objects.filter(is_deleted=False).first()
    if first_test:
        return redirect('laboratory:edit', pk=first_test.pk)
    messages.warning(request, "No lab tests registered yet. Please create a lab test first.")
    return redirect('laboratory:list')
"""

    patients_views = """from django.shortcuts import render, redirect, get_object_or_404

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
    patient = get_object_or_404(Patient, pk=pk, is_deleted=False)
    results = patient.test_results.select_related('test').order_by('-performed_date', 'test__name')
    return render(request, 'laboratory/patient_results_detail.html', {
        'patient': patient,
        'results': results
    })
"""

    orders_views = """from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

def pending_orders(request):
    from orders.models import Order
    orders = Order.objects.filter(test__isnull=False, status='pending').order_by('order_date')
    return render(request, 'laboratory/pending_orders.html', {'orders': orders})

def fulfill_order(request, pk):
    from orders.models import Order
    from laboratory.forms import FulfillOrderForm
    order = get_object_or_404(Order, pk=pk, test__isnull=False)
    
    if request.method == 'POST':
        form = FulfillOrderForm(request.POST, order=order)
        if form.is_valid():
            results = form.save_results(request.user)
            
            order.status = 'completed'
            order.save()
            
            messages.success(request, f"Order fulfilled for {order.patient}.")
            return redirect('laboratory:pending_orders')
    else:
        form = FulfillOrderForm(order=order)
        
    return render(request, 'laboratory/fulfill_order.html', {
        'form': form,
        'order': order
    })
"""

    with open(os.path.join(base_dir, 'views', 'tests.py'), 'w') as f:
        f.write(tests_views)
        
    with open(os.path.join(base_dir, 'views', 'patients.py'), 'w') as f:
        f.write(patients_views)

    with open(os.path.join(base_dir, 'views', 'orders.py'), 'w') as f:
        f.write(orders_views)

    with open(os.path.join(base_dir, 'views', '__init__.py'), 'w') as f:
        f.write("from .tests import *\nfrom .patients import *\nfrom .orders import *\n")


split_models()
split_views()
print("Successfully split models and views")
