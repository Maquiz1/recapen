from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from patients.models import Patient
from .models import Encounter

def log_followup(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    
    if request.method == 'POST':
        visit_nature = request.POST.get('visit_nature')
        if visit_nature in ['scheduled', 'unscheduled']:
            encounter = Encounter.objects.create(
                patient=patient,
                encounter_type='followup',
                visit_nature=visit_nature,
                status='arrived',
                doctor=request.user if request.user.is_authenticated else None
            )
            messages.success(request, f"Logged a new {visit_nature} follow-up encounter for {patient}.")
        else:
            messages.error(request, "Invalid visit nature selected.")
            
    return redirect('encounters:encounter_detail', encounter_id=encounter.pk)

def encounter_detail(request, encounter_id):
    from study_config.models import FollowUpRule
    
    encounter = get_object_or_404(Encounter, pk=encounter_id)
    patient = encounter.patient
    
    required_forms = set()
    if patient.status == 'enrolled' and encounter.visit_nature:
        if hasattr(patient, 'enrollment') and patient.enrollment.cohort:
            cohort_code = patient.enrollment.cohort
            # Match the cohort code to the FollowUpRule choices
            rules = FollowUpRule.objects.filter(
                cohort=cohort_code.lower(), 
                encounter_type=encounter.encounter_type,
                visit_nature=encounter.visit_nature
            )
            for rule in rules:
                for form in rule.required_forms.all():
                    required_forms.add(form)
                    
    has_vitals = hasattr(encounter, 'vitals')
    has_hospitalization = hasattr(encounter, 'hospitalization')
    has_risk = hasattr(encounter, 'risk')
    has_socioeconomic = hasattr(encounter, 'socioeconomic')
    has_treatment = hasattr(encounter, 'treatment')
    has_clinical_history = hasattr(encounter, 'clinical_history')
    has_symptom = hasattr(encounter, 'symptom')
    has_complications = hasattr(encounter, 'complications')
    has_school_home = hasattr(encounter, 'school_home_assessment')
    
    # Check if a pharmacy order (prescription) exists
    has_prescriptions = encounter.prescriptions.exists()
    prescriptions = encounter.prescriptions.all()
    
    from medications.forms import PrescriptionForm
    prescription_form = PrescriptionForm()
                    
    return render(request, 'encounters/encounter_detail.html', {
        'encounter': encounter,
        'patient': patient,
        'prescriptions': prescriptions,
        'prescription_form': prescription_form,
        'required_forms': list(required_forms),
        'has_vitals': has_vitals,
        'has_hospitalization': has_hospitalization,
        'has_prescriptions': has_prescriptions,
        'has_risk': has_risk,
        'has_socioeconomic': has_socioeconomic,
        'has_treatment': has_treatment,
        'has_clinical_history': has_clinical_history,
        'has_symptom': has_symptom,
        'has_complications': has_complications,
        'has_school_home': has_school_home,
    })

def update_visit_nature(request, encounter_id):
    if request.method == 'POST':
        encounter = get_object_or_404(Encounter, pk=encounter_id)
        new_nature = request.POST.get('visit_nature')
        new_type = request.POST.get('encounter_type')
        
        updated = False
        if new_nature in ['scheduled', 'unscheduled']:
            encounter.visit_nature = new_nature
            updated = True
            
        # Get valid encounter types from model choices
        valid_types = dict(Encounter.ENCOUNTER_TYPE_CHOICES).keys()
        if new_type and new_type in valid_types:
            encounter.encounter_type = new_type
            updated = True
            
        if updated:
            if request.user.is_authenticated:
                encounter.updated_by = request.user
            encounter.save()
            messages.success(request, f"Encounter details updated.")
            
        return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
    return redirect('patients:list')

def log_scheduled_visit(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        from appointments.models import Appointment
        appointment = get_object_or_404(Appointment, pk=appointment_id, patient=patient)
        
        if appointment.status in ['scheduled', 'missed']:
            appointment.status = 'arrived'
            
            encounter = Encounter.objects.create(
                patient=patient,
                doctor=request.user if request.user.is_authenticated else None,
                status='in_progress',
                encounter_type='followup',
                visit_nature='scheduled',
                created_by=request.user if request.user.is_authenticated else None,
                updated_by=request.user if request.user.is_authenticated else None
            )
            
            appointment.encounter = encounter
            appointment.save()
            
            messages.success(request, f"Logged scheduled follow-up: {appointment.reason}")
            return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
        else:
            messages.error(request, "This schedule cannot be checked in.")
            
    return redirect('patients:profile', pk=patient_id)

def missing_meds_list(request):
    """
    List of encounters missing medications (prescriptions).
    """
    encounters = Encounter.objects.exclude(prescriptions__isnull=False).distinct().order_by('-start_time')
    return render(request, 'encounters/missing_meds_list.html', {
        'encounters': encounters,
    })

from clinical.models import Prescription
from clinical.forms import PrescriptionForm

def manage_prescription(request, encounter_id, prescription_id=None):
    encounter = get_object_or_404(Encounter, pk=encounter_id)
    
    if request.method == 'POST':
        if prescription_id:
            prescription = get_object_or_404(Prescription, pk=prescription_id, encounter=encounter)
            # Check for delete
            if 'delete' in request.POST:
                prescription.delete()
                messages.success(request, "Prescription deleted.")
                return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
            form = PrescriptionForm(request.POST, instance=prescription)
            action_msg = "updated"
        else:
            form = PrescriptionForm(request.POST)
            action_msg = "added"
            
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.encounter = encounter
            prescription.patient = encounter.patient
            prescription.save()
            messages.success(request, f"Prescription {action_msg} successfully.")
        else:
            messages.error(request, "Error saving prescription. Please check the form.")
            
    return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
