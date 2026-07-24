from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from laboratory.models import LaboratoryTest
from .forms import CardiologyTestForm
from patients.models import Patient

def test_list(request):
    tests = LaboratoryTest.objects.filter(is_active=True).order_by('name')
    return render(request, 'cardiology/test_list.html', {'tests': tests})

def test_create(request):
    if request.method == 'POST':
        form = CardiologyTestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            if request.user.is_authenticated:
                test.created_by = request.user
                test.updated_by = request.user
            test.save()
            form.save_m2m() # Saves diseases relation
            messages.success(request, f"Cardiology test '{test.name}' registered successfully.")
            return redirect('cardiology:list')
    else:
        form = CardiologyTestForm()
    return render(request, 'cardiology/test_form.html', {'form': form, 'title': 'Add Cardiology Test'})

def test_edit(request, pk):
    test = get_object_or_404(LaboratoryTest, pk=pk)
    if request.method == 'POST':
        form = CardiologyTestForm(request.POST, instance=test)
        if form.is_valid():
            t = form.save(commit=False)
            if request.user.is_authenticated:
                t.updated_by = request.user
            t.save()
            form.save_m2m()
            messages.success(request, f"Cardiology test '{t.name}' updated successfully.")
            return redirect('cardiology:list')
    else:
        form = CardiologyTestForm(instance=test)
    return render(request, 'cardiology/test_form.html', {'form': form, 'title': 'Edit Cardiology Test', 'test': test})

def test_edit_redirect(request):
    first_test = LaboratoryTest.objects.filter(is_active=True).first()
    if first_test:
        return redirect('cardiology:edit', pk=first_test.pk)
    messages.warning(request, "No cardiology tests registered yet. Please create a test first.")
    return redirect('cardiology:list')

def patient_results_list(request):
    # Show patients that have been screened (i.e. tests ordered) or diagnosed
    patients = Patient.objects.filter(status__in=['screened', 'diagnosed', 'enrolled'], is_deleted=False).order_by('-created_at')
    return render(request, 'cardiology/patient_results_list.html', {'patients': patients})

def patients_with_results(request):
    # Patients who have cardiology test results
    patients = Patient.objects.filter(test_results__test__is_deleted=False).distinct().order_by('-created_at')
    return render(request, 'cardiology/patients_results_list.html', {'patients': patients})

def patient_results_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk, is_deleted=False)
    results = patient.test_results.filter(test__).select_related('test').order_by('-performed_date', 'test__name')
    return render(request, 'cardiology/patient_results_detail.html', {
        'patient': patient,
        'results': results
    })

def pending_orders(request):
    from orders.models import Order
    orders = Order.objects.filter(order_type='cardiology', status='pending').order_by('order_date')
    return render(request, 'cardiology/pending_orders.html', {'orders': orders})

def fulfill_order(request, pk):
    from orders.models import Order
    from .forms_order import FulfillOrderForm
    order = get_object_or_404(Order, pk=pk, order_type='cardiology')
    
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
