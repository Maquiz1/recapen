from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from laboratory.models import LabTest
from .forms import RadiologyTestForm
from patients.models import Patient

def test_list(request):
    tests = LabTest.objects.filter(is_active=True, category='radiology').order_by('name')
    return render(request, 'radiology/test_list.html', {'tests': tests})

def test_create(request):
    if request.method == 'POST':
        form = RadiologyTestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            if request.user.is_authenticated:
                test.created_by = request.user
                test.updated_by = request.user
            test.save()
            form.save_m2m() # Saves diseases relation
            messages.success(request, f"Radiology/Imaging test '{test.name}' registered successfully.")
            return redirect('radiology:list')
    else:
        form = RadiologyTestForm()
    return render(request, 'radiology/test_form.html', {'form': form, 'title': 'Add Radiology Test'})

def test_edit(request, pk):
    test = get_object_or_404(LabTest, pk=pk, category='radiology')
    if request.method == 'POST':
        form = RadiologyTestForm(request.POST, instance=test)
        if form.is_valid():
            t = form.save(commit=False)
            if request.user.is_authenticated:
                t.updated_by = request.user
            t.save()
            form.save_m2m()
            messages.success(request, f"Radiology test '{t.name}' updated successfully.")
            return redirect('radiology:list')
    else:
        form = RadiologyTestForm(instance=test)
    return render(request, 'radiology/test_form.html', {'form': form, 'title': 'Edit Radiology Test', 'test': test})

def test_edit_redirect(request):
    first_test = LabTest.objects.filter(is_active=True, category='radiology').first()
    if first_test:
        return redirect('radiology:edit', pk=first_test.pk)
    messages.warning(request, "No radiology tests registered yet. Please create a test first.")
    return redirect('radiology:list')

def patient_results_list(request):
    # Show patients that have been screened (i.e. tests ordered) or diagnosed
    # Note: A real app might check if they specifically ordered radiology tests.
    patients = Patient.objects.filter(status__in=['screened', 'diagnosed', 'enrolled'], is_deleted=False).order_by('-created_at')
    return render(request, 'radiology/patient_results_list.html', {'patients': patients})

def patients_with_results(request):
    # Patients who have radiology test results
    patients = Patient.objects.filter(test_results__test__category='radiology', is_deleted=False).distinct().order_by('-created_at')
    return render(request, 'radiology/patients_results_list.html', {'patients': patients})

def patient_results_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk, is_deleted=False)
    results = patient.test_results.filter(test__category='radiology').select_related('test').order_by('-performed_date', 'test__name')
    return render(request, 'radiology/patient_results_detail.html', {
        'patient': patient,
        'results': results
    })
