from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from encounters.models import Encounter
from clinical.forms import VitalsForm, HospitalizationForm, RiskForm, SocioeconomicForm, TreatmentForm, HistoryForm, SymptomForm, ComplicationsForm, SchoolHomeAssessmentForm

def fill_form(request, encounter_id, form_code):
    encounter = get_object_or_404(Encounter, pk=encounter_id)
    form_code_lower = form_code.lower()
    
    if form_code_lower in ['vitals', 'vt']:
        instance = getattr(encounter, 'vitals', None)
        if request.method == 'POST':
            form = VitalsForm(request.POST, instance=instance)
            if form.is_valid():
                vitals = form.save(commit=False)
                vitals.encounter = encounter
                vitals.save()
                messages.success(request, "Vitals recorded successfully.")
                return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
        else:
            form = VitalsForm(instance=instance)
            
        return render(request, 'clinical/vitals.html', {
            'form': form,
            'encounter': encounter,
            'patient': encounter.patient,
        })
        
    elif form_code_lower in ['hospitalization', 'hosp']:
        instance = getattr(encounter, 'hospitalization', None)
        if request.method == 'POST':
            form = HospitalizationForm(request.POST, instance=instance)
            if form.is_valid():
                hosp = form.save(commit=False)
                hosp.encounter = encounter
                hosp.save()
                messages.success(request, "Hospitalization recorded successfully.")
                return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
        else:
            form = HospitalizationForm(instance=instance)
            
        return render(request, 'clinical/hospitalization.html', {
            'form': form,
            'encounter': encounter,
            'patient': encounter.patient,
        })
        
    elif form_code_lower in ['risk', 'risks']:
        instance = getattr(encounter, 'risk', None)
        if request.method == 'POST':
            form = RiskForm(request.POST, instance=instance)
            if form.is_valid():
                risk = form.save(commit=False)
                risk.encounter = encounter
                risk.save()
                messages.success(request, "Risk recorded successfully.")
                return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
        else:
            form = RiskForm(instance=instance)
            
        return render(request, 'clinical/risk.html', {
            'form': form,
            'encounter': encounter,
            'patient': encounter.patient,
        })
        
    elif form_code_lower in ['socioeconomic', 'se']:
        instance = getattr(encounter, 'socioeconomic', None)
        if request.method == 'POST':
            form = SocioeconomicForm(request.POST, instance=instance)
            if form.is_valid():
                se = form.save(commit=False)
                se.encounter = encounter
                se.save()
                messages.success(request, "Socioeconomic recorded successfully.")
                return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
        else:
            form = SocioeconomicForm(instance=instance)
            
        return render(request, 'clinical/socioeconomic.html', {
            'form': form,
            'encounter': encounter,
            'patient': encounter.patient,
        })
        
    elif form_code_lower in ['treatment', 'tx']:
        instance = getattr(encounter, 'treatment', None)
        if request.method == 'POST':
            form = TreatmentForm(request.POST, instance=instance)
            if form.is_valid():
                tx = form.save(commit=False)
                tx.encounter = encounter
                tx.save()
                messages.success(request, "Treatment recorded successfully.")
                return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
        else:
            form = TreatmentForm(instance=instance)
            
        return render(request, 'clinical/treatment.html', {
            'form': form,
            'encounter': encounter,
            'patient': encounter.patient,
        })

    elif form_code_lower in ['history', 'hist']:
        instance = getattr(encounter, 'clinical_history', None)
        if request.method == 'POST':
            form = HistoryForm(request.POST, instance=instance)
            if form.is_valid():
                hist = form.save(commit=False)
                hist.encounter = encounter
                hist.save()
                messages.success(request, "History recorded successfully.")
                return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
        else:
            form = HistoryForm(instance=instance)
            
        return render(request, 'clinical/history.html', {
            'form': form,
            'encounter': encounter,
            'patient': encounter.patient,
        })

    elif form_code_lower in ['symptom', 'symptoms', 'symp']:
        instance = getattr(encounter, 'symptom', None)
        if request.method == 'POST':
            form = SymptomForm(request.POST, instance=instance)
            if form.is_valid():
                symp = form.save(commit=False)
                symp.encounter = encounter
                symp.save()
                messages.success(request, "Symptom recorded successfully.")
                return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
        else:
            form = SymptomForm(instance=instance)
            
        return render(request, 'clinical/symptom.html', {
            'form': form,
            'encounter': encounter,
            'patient': encounter.patient,
        })

    elif form_code_lower in ['complications', 'comp']:
        instance = getattr(encounter, 'complications', None)
        if request.method == 'POST':
            form = ComplicationsForm(request.POST, instance=instance)
            if form.is_valid():
                comp = form.save(commit=False)
                comp.encounter = encounter
                comp.save()
                messages.success(request, "Complications recorded successfully.")
                return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
        else:
            form = ComplicationsForm(instance=instance)
            
        return render(request, 'clinical/complications.html', {
            'form': form,
            'encounter': encounter,
            'patient': encounter.patient,
        })
        
    elif form_code_lower in ['school_home_assessment', 'schoolhomeassessment', 'schoolhome']:
        instance = getattr(encounter, 'school_home_assessment', None)
        if request.method == 'POST':
            form = SchoolHomeAssessmentForm(request.POST, instance=instance)
            if form.is_valid():
                assessment = form.save(commit=False)
                assessment.encounter = encounter
                assessment.save()
                messages.success(request, "SchoolHomeAssessment recorded successfully.")
                return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
        else:
            form = SchoolHomeAssessmentForm(instance=instance)
            
        return render(request, 'clinical/school_home_assessment.html', {
            'form': form,
            'encounter': encounter,
            'patient': encounter.patient,
        })
        
    else:
        messages.error(request, f"Form logic for {form_code} is not yet implemented.")
        return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
