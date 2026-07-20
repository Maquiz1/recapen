from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import LabTest
from .forms import LabTestForm

def test_list(request):
    tests = LabTest.objects.filter(is_active=True).order_by('category', 'name')
    return render(request, 'laboratory/test_list.html', {'tests': tests})

def test_create(request):
    if request.method == 'POST':
        form = LabTestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            if request.user.is_authenticated:
                test.created_by = request.user
                test.updated_by = request.user
            test.save()
            form.save_m2m() # Saves diseases relation
            messages.success(request, f"Lab test '{test.name}' registered successfully.")
            return redirect('laboratory:list')
    else:
        form = LabTestForm()
    return render(request, 'laboratory/test_form.html', {'form': form, 'title': 'Add Lab Test'})

def test_edit(request, pk):
    test = get_object_or_404(LabTest, pk=pk)
    if request.method == 'POST':
        form = LabTestForm(request.POST, instance=test)
        if form.is_valid():
            t = form.save(commit=False)
            if request.user.is_authenticated:
                t.updated_by = request.user
            t.save()
            form.save_m2m()
            messages.success(request, f"Lab test '{t.name}' updated successfully.")
            return redirect('laboratory:list')
    else:
        form = LabTestForm(instance=test)
    return render(request, 'laboratory/test_form.html', {'form': form, 'title': 'Edit Lab Test', 'test': test})

def test_edit_redirect(request):
    first_test = LabTest.objects.filter(is_active=True).first()
    if first_test:
        return redirect('laboratory:edit', pk=first_test.pk)
    messages.warning(request, "No lab tests registered yet. Please create a lab test first.")
    return redirect('laboratory:list')

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
