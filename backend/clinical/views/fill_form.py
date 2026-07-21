from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from encounters.models import Encounter
from clinical.forms import VitalsForm, HospitalizationForm, RiskForm, SocioeconomicForm, TreatmentForm

def fill_form(request, encounter_id, form_code):
    encounter = get_object_or_404(Encounter, pk=encounter_id)
    
    if form_code == 'vitals':
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
        
    elif form_code == 'hospitalization':
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
        
    elif form_code == 'risk':
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
        
    elif form_code == 'socioeconomic':
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
        
    elif form_code == 'treatment':
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
        
    else:
        messages.error(request, f"Form logic for {form_code} is not yet implemented.")
        return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
