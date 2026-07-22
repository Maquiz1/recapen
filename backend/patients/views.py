from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Patient, Screening, Diagnosis, Enrollment
from .forms import PatientForm, ScreeningForm, SCDInvestigationForm, DMInvestigationForm, CardiacInvestigationForm, DiagnosisForm, EnrollmentForm

def patient_list(request):
    patients = Patient.objects.filter(is_deleted=False).order_by('-created_at')
    return render(request, 'patients/patient_list.html', {'patients': patients})

def patient_diagnosis_list(request):
    # Only show patients that have been screened, diagnosed, or enrolled.
    # The primary action will be to perform diagnosis.
    patients = Patient.objects.filter(is_deleted=False, status__in=['screened', 'diagnosed', 'enrolled']).order_by('-created_at')
    return render(request, 'patients/patient_diagnosis_list.html', {'patients': patients})

def patient_register(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            if request.user.is_authenticated:
                patient.created_by = request.user
                patient.updated_by = request.user
            patient.status = 'registered'
            patient.save()
            messages.success(request, f"Patient {patient} registered successfully.")
            return redirect('patients:screening', pk=patient.pk)
    else:
        form = PatientForm()
    return render(request, 'patients/patient_register.html', {'form': form})

def patient_screening(request, pk):
    patient = get_object_or_404(Patient, pk=pk, is_deleted=False)
    screening, created = Screening.objects.get_or_create(patient=patient)
    
    if request.method == 'POST':
        form = ScreeningForm(request.POST, instance=screening)
        if form.is_valid():
            screening = form.save(commit=False)
            if request.user.is_authenticated:
                screening.created_by = request.user
                screening.updated_by = request.user
            # The custom form save method handles M2M saving even when commit=False,
            # but we explicitly save it here just to be safe.
            screening = form.save(commit=True)
            
            # Generate Encounter
            from encounters.models import Encounter
            from orders.models import Order
            
            encounter, enc_created = Encounter.objects.get_or_create(
                patient=patient,
                status='in_progress',
                defaults={
                    'doctor': request.user if request.user.is_authenticated else None,
                    'encounter_type': 'initial' if patient.status == 'registered' else 'followup'
                }
            )
            
            # Generate Orders
            for test in screening.ordered_tests.all():
                Order.objects.get_or_create(
                    encounter=encounter,
                    patient=patient,
                    test=test,
                    defaults={
                        'ordering_doctor': request.user if request.user.is_authenticated else None,
                        'order_type': test.category,
                        'status': 'pending'
                    }
                )
            
            patient.status = 'screened'
            patient.save()
            
            messages.success(request, f"Screening results saved and Orders generated for {patient}.")
            return redirect('patients:investigation', pk=patient.pk)
    else:
        form = ScreeningForm(instance=screening)
        
    return render(request, 'patients/patient_screening.html', {
        'form': form,
        'patient': patient
    })

def patient_investigation(request, pk):
    patient = get_object_or_404(Patient, pk=pk, is_deleted=False)
    screening = get_object_or_404(Screening, patient=patient)
    
    scd_form = None
    dm_form = None
    cardiac_form = None
    
    if screening.suspect_scd and (screening.order_scd_lab or screening.order_scd_radiology or screening.order_scd_echo or screening.order_scd_screening):
        scd_form = SCDInvestigationForm(request.POST or None, patient=patient, prefix='scd')
        
    if screening.suspect_dm and (screening.order_dm_hba1c or screening.order_dm_c_peptide or screening.order_dm_creatinine or screening.order_dm_urea or screening.order_dm_rbg or screening.order_dm_fbg):
        dm_form = DMInvestigationForm(request.POST or None, patient=patient, prefix='dm')
        
    if screening.suspect_cardiac and (screening.order_cardiac_lab or screening.order_cardiac_echo or screening.order_cardiac_ecg or screening.order_cardiac_xray):
        cardiac_form = CardiacInvestigationForm(request.POST or None, patient=patient, prefix='cardiac')
        
    if request.method == 'POST':
        valid = True
        if scd_form and not scd_form.is_valid():
            valid = False
        if dm_form and not dm_form.is_valid():
            valid = False
        if cardiac_form and not cardiac_form.is_valid():
            valid = False
            
        if valid:
            if scd_form:
                scd_form.save(user=request.user)
            if dm_form:
                dm_form.save(user=request.user)
            if cardiac_form:
                cardiac_form.save(user=request.user)
                
            messages.success(request, f"Investigation results updated for {patient}.")
            return redirect('patients:diagnosis', pk=patient.pk)
    
    return render(request, 'patients/patient_investigation.html', {
        'patient': patient,
        'screening': screening,
        'scd_form': scd_form,
        'dm_form': dm_form,
        'cardiac_form': cardiac_form
    })

def patient_diagnosis(request, pk):
    patient = get_object_or_404(Patient, pk=pk, is_deleted=False)
    diagnosis, _ = Diagnosis.objects.get_or_create(patient=patient)
    enrollment, _ = Enrollment.objects.get_or_create(patient=patient)
    
    if request.method == 'POST':
        c_form = DiagnosisForm(request.POST, instance=diagnosis, prefix='consult')
        e_form = EnrollmentForm(request.POST, instance=enrollment, prefix='enroll')
        
        if c_form.is_valid() and e_form.is_valid():
            c = c_form.save(commit=False)
            if request.user.is_authenticated:
                c.created_by = request.user
                c.updated_by = request.user
            c.save()
            
            e = e_form.save(commit=False)
            if request.user.is_authenticated:
                e.created_by = request.user
                e.updated_by = request.user
            e.save()
            
            if e.is_eligible:
                patient.status = 'diagnosed'
                patient.save()
                
                # Finish the encounter
                from encounters.models import Encounter
                from django.utils import timezone
                encounter = Encounter.objects.filter(patient=patient, status='in_progress').first()
                if encounter:
                    encounter.status = 'finished'
                    encounter.end_time = timezone.now()
                    encounter.save()
                    
                messages.success(request, f"Diagnosis recorded. {patient} is eligible for enrollment.")
                return redirect('patients:diagnosis_list')
            else:
                patient.status = 'ineligible'
                patient.save()
                
                # Finish the encounter
                from encounters.models import Encounter
                from django.utils import timezone
                encounter = Encounter.objects.filter(patient=patient, status='in_progress').first()
                if encounter:
                    encounter.status = 'finished'
                    encounter.end_time = timezone.now()
                    encounter.save()
                    
                messages.warning(request, f"Patient {patient} marked as ineligible for program.")
                return redirect('patients:diagnosis_list')
    else:
        c_form = DiagnosisForm(instance=diagnosis, prefix='consult')
        e_form = EnrollmentForm(instance=enrollment, prefix='enroll')
        
    return render(request, 'patients/patient_diagnosis.html', {
        'patient': patient,
        'c_form': c_form,
        'e_form': e_form
    })

def patient_enrollment(request, pk):
    patient = get_object_or_404(Patient, pk=pk, is_deleted=False)
    enrollment = get_object_or_404(Enrollment, patient=patient)
    
    if request.method == 'POST':
        form = EnrollmentForm(request.POST, instance=enrollment, prefix='enroll')
        if form.is_valid():
            e = form.save(commit=False)
            e.save()
            patient.status = 'enrolled'
            patient.save()
            messages.success(request, f"Patient {patient} successfully enrolled in cohort: {e.get_cohort_display()}.")
            return redirect('patients:list')
    else:
        form = EnrollmentForm(instance=enrollment, prefix='enroll')
        
    return render(request, 'patients/patient_enrollment.html', {
        'patient': patient,
        'form': form
    })

def patient_profile(request, pk):
    patient = get_object_or_404(Patient, pk=pk, is_deleted=False)
    pending_orders = patient.orders.filter(status='pending')
    pending_orders_exist = pending_orders.exists()
    return render(request, 'patients/patient_profile.html', {
        'patient': patient,
        'pending_orders': pending_orders,
        'pending_orders_exist': pending_orders_exist,
    })

def patient_dashboard(request, pk):
    patient = get_object_or_404(Patient, pk=pk, is_deleted=False)
    pending_orders = patient.orders.filter(status='pending')
    pending_orders_exist = pending_orders.exists()
    return render(request, 'patients/patient_profile.html', {
        'patient': patient,
        'is_dashboard': True,
        'pending_orders': pending_orders,
        'pending_orders_exist': pending_orders_exist,
    })

def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk, is_deleted=False)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            p = form.save(commit=False)
            if request.user.is_authenticated:
                p.updated_by = request.user
            p.save()
            messages.success(request, f"Patient {p} updated successfully.")
            return redirect('patients:list')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patients/patient_edit.html', {'form': form, 'patient': patient})

def my_patients(request):
    patients = Patient.objects.filter(is_deleted=False).order_by('-created_at')
    
    active_count = patients.filter(status='enrolled').count()
    inactive_count = patients.exclude(status='enrolled').count()
    
    return render(request, 'patients/my_patients.html', {
        'patients': patients,
        'active_count': active_count,
        'inactive_count': inactive_count,
    })

def patient_dashboard_redirect(request):
    first_patient = Patient.objects.filter(is_deleted=False).order_by('-created_at').first()
    if first_patient:
        return redirect('patients:dashboard', pk=first_patient.pk)
    messages.warning(request, "No patients registered yet. Please add a patient first.")
    return redirect('patients:list')

def patient_profile_redirect(request):
    first_patient = Patient.objects.filter(is_deleted=False).order_by('-created_at').first()
    if first_patient:
        return redirect('patients:profile', pk=first_patient.pk)
    messages.warning(request, "No patients registered yet. Please add a patient first.")
    return redirect('patients:list')

def patient_edit_redirect(request):
    first_patient = Patient.objects.filter(is_deleted=False).order_by('-created_at').first()
    if first_patient:
        return redirect('patients:edit', pk=first_patient.pk)
    messages.warning(request, "No patients registered yet. Please add a patient first.")
    return redirect('patients:list')
