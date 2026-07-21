from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from encounters.models import Encounter
from clinical.forms import VitalsForm, HospitalizationForm, RiskForm, SocioeconomicForm, TreatmentForm, HistoryForm, SymptomForm, ComplicationsForm, SchoolHomeAssessmentForm

def fill_form(request, encounter_id, form_code):
    encounter = get_object_or_404(Encounter, pk=encounter_id)
    form_code_lower = form_code.lower()
    
    if form_code_lower in ['vitals', 'vt']:
        if hasattr(encounter, 'vitals'):
            messages.info(request, "Vitals form is already completed for this encounter.")
            return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
            
        if request.method == 'POST':
            form = VitalsForm(request.POST)
            if form.is_valid():
                vitals = form.save(commit=False)
                vitals.encounter = encounter
                vitals.save()
                messages.success(request, "Vitals recorded successfully.")
                return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
        else:
            form = VitalsForm()
            
        return render(request, 'clinical/vitals.html', {
            'form': form,
            'encounter': encounter,
            'patient': encounter.patient,
        })
        
    elif form_code_lower in ['hospitalization', 'hosp']:
        if hasattr(encounter, 'hospitalization'):
            messages.info(request, "Hospitalization form is already completed for this encounter.")
            return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
            
        if request.method == 'POST':
            form = HospitalizationForm(request.POST)
            if form.is_valid():
                hosp = form.save(commit=False)
                hosp.encounter = encounter
                hosp.save()
                messages.success(request, "Hospitalization recorded successfully.")
                return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
        else:
            form = HospitalizationForm()
            
        return render(request, 'clinical/hospitalization.html', {
            'form': form,
            'encounter': encounter,
            'patient': encounter.patient,
        })
        
    elif form_code_lower in ['risk', 'risks']:
        if hasattr(encounter, 'risk'):
            messages.info(request, "Risk Factors form is already completed for this encounter.")
            return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
            
        if request.method == 'POST':
            form = RiskForm(request.POST)
            if form.is_valid():
                risk = form.save(commit=False)
                risk.encounter = encounter
                risk.save()
                messages.success(request, "Risk Factors recorded successfully.")
                return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
        else:
            form = RiskForm()
            
        return render(request, 'clinical/risk.html', {
            'form': form,
            'encounter': encounter,
            'patient': encounter.patient,
        })
        
    elif form_code_lower in ['socioeconomic', 'se']:
        if hasattr(encounter, 'socioeconomic'):
            messages.info(request, "Socioeconomic form is already completed for this encounter.")
            return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
            
        if request.method == 'POST':
            form = SocioeconomicForm(request.POST)
            if form.is_valid():
                se = form.save(commit=False)
                se.encounter = encounter
                se.save()
                messages.success(request, "Socioeconomic profile recorded successfully.")
                return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
        else:
            form = SocioeconomicForm()
            
        return render(request, 'clinical/socioeconomic.html', {
            'form': form,
            'encounter': encounter,
            'patient': encounter.patient,
        })
        
    elif form_code_lower in ['treatment', 'tx']:
        if hasattr(encounter, 'treatment'):
            messages.info(request, "Treatment plan form is already completed for this encounter.")
            return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
            
        if request.method == 'POST':
            form = TreatmentForm(request.POST)
            if form.is_valid():
                tx = form.save(commit=False)
                tx.encounter = encounter
                tx.save()
                messages.success(request, "Treatment plan recorded successfully.")
                return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
        else:
            form = TreatmentForm()
            
        return render(request, 'clinical/treatment.html', {
            'form': form,
            'encounter': encounter,
            'patient': encounter.patient,
        })

    elif form_code_lower in ['history', 'hist']:
        if hasattr(encounter, 'clinical_history'):
            messages.info(request, "History form is already completed for this encounter.")
            return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
            
        if request.method == 'POST':
            form = HistoryForm(request.POST)
            if form.is_valid():
                hist = form.save(commit=False)
                hist.encounter = encounter
                hist.save()
                messages.success(request, "Medical history recorded successfully.")
                return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
        else:
            form = HistoryForm()
            
        return render(request, 'clinical/history.html', {
            'form': form,
            'encounter': encounter,
            'patient': encounter.patient,
        })

    elif form_code_lower in ['symptom', 'symptoms', 'symp']:
        if hasattr(encounter, 'symptom'):
            messages.info(request, "Symptoms form is already completed for this encounter.")
            return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
            
        if request.method == 'POST':
            form = SymptomForm(request.POST)
            if form.is_valid():
                symp = form.save(commit=False)
                symp.encounter = encounter
                symp.save()
                messages.success(request, "Symptom details recorded successfully.")
                return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
        else:
            form = SymptomForm()
            
        return render(request, 'clinical/symptom.html', {
            'form': form,
            'encounter': encounter,
            'patient': encounter.patient,
        })

    elif form_code_lower in ['complications', 'comp']:
        if hasattr(encounter, 'complications'):
            messages.info(request, "Complications form is already completed for this encounter.")
            return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
            
        if request.method == 'POST':
            form = ComplicationsForm(request.POST)
            if form.is_valid():
                comp = form.save(commit=False)
                comp.encounter = encounter
                comp.save()
                messages.success(request, "Complications details recorded successfully.")
                return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
        else:
            form = ComplicationsForm()
            
        return render(request, 'clinical/complications.html', {
            'form': form,
            'encounter': encounter,
            'patient': encounter.patient,
        })
        
    elif form_code_lower in ['school_home_assessment', 'schoolhomeassessment', 'schoolhome']:
        if hasattr(encounter, 'school_home_assessment'):
            messages.info(request, "School & Home Assessment form is already completed for this encounter.")
            return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
            
        if request.method == 'POST':
            form = SchoolHomeAssessmentForm(request.POST)
            if form.is_valid():
                assessment = form.save(commit=False)
                assessment.encounter = encounter
                assessment.save()
                messages.success(request, "School & Home Assessment recorded successfully.")
                return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
        else:
            form = SchoolHomeAssessmentForm()
            
        return render(request, 'clinical/school_home_assessment.html', {
            'form': form,
            'encounter': encounter,
            'patient': encounter.patient,
        })
        
    else:
        messages.error(request, f"Form logic for {form_code} is not yet implemented.")
        return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
