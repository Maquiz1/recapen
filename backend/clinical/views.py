from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from encounters.models import Encounter
from .forms import VitalsForm

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
            
        from .forms import HospitalizationForm
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
        
    else:
        messages.error(request, f"Form logic for {form_code} is not yet implemented.")
        return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
