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
    
    required_forms = []
    if patient.status == 'enrolled' and encounter.visit_nature:
        # Determine cohort from patient's latest disease assignment if necessary, 
        # For simplicity, assuming the patient's primary disease maps to the cohort.
        # Recap: Patient disease is captured in Patient.disease or similar?
        # Wait, how did we link patient to disease?
        pass
        
    return render(request, 'encounters/encounter_detail.html', {
        'encounter': encounter,
        'patient': patient,
        'required_forms': required_forms,
    })
