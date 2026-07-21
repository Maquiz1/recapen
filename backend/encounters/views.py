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
        patient_cohorts = patient.confirmed_diseases.values_list('code', flat=True)
        for cohort_code in patient_cohorts:
            # Match the cohort code (e.g. 'SCD', 'DM') to the FollowUpRule choices ('scd', 'dm')
            rules = FollowUpRule.objects.filter(
                cohort=cohort_code.lower(), 
                visit_nature=encounter.visit_nature
            )
            for rule in rules:
                for form in rule.required_forms.all():
                    required_forms.add(form)
                    
    has_scd_vitals = hasattr(encounter, 'scd_vitals')
                    
    return render(request, 'encounters/encounter_detail.html', {
        'encounter': encounter,
        'patient': patient,
        'required_forms': list(required_forms),
        'has_scd_vitals': has_scd_vitals,
    })
