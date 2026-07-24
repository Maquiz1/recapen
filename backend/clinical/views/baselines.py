from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from patients.models import Enrollment, Patient
from clinical.models.baselines import SickleCellBaseline, DiabetesBaseline, CardiacBaseline
from clinical.forms.baselines import SickleCellBaselineForm, DiabetesBaselineForm, CardiacBaselineForm

def baseline_forms(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, pk=enrollment_id)
    patient = enrollment.patient
    
    # We will determine which forms to show based on the cohort
    # Actually, enrollment cohort only allows ONE right now. But in case it changes, we check it.
    show_scd = enrollment.cohort == 'scd'
    show_dm = enrollment.cohort == 'dm'
    show_cardiac = enrollment.cohort == 'cardiac'

    if show_scd:
        scd_baseline, _ = SickleCellBaseline.objects.get_or_create(enrollment=enrollment)
    if show_dm:
        dm_baseline, _ = DiabetesBaseline.objects.get_or_create(enrollment=enrollment)
    if show_cardiac:
        cardiac_baseline, _ = CardiacBaseline.objects.get_or_create(enrollment=enrollment)

    if request.method == 'POST':
        valid = True
        if show_scd:
            scd_form = SickleCellBaselineForm(request.POST, instance=scd_baseline, prefix='scd')
            if scd_form.is_valid():
                scd_form.save()
            else:
                valid = False
        else:
            scd_form = None

        if show_dm:
            dm_form = DiabetesBaselineForm(request.POST, instance=dm_baseline, prefix='dm')
            if dm_form.is_valid():
                dm_form.save()
            else:
                valid = False
        else:
            dm_form = None

        if show_cardiac:
            cardiac_form = CardiacBaselineForm(request.POST, instance=cardiac_baseline, prefix='cardiac')
            if cardiac_form.is_valid():
                cardiac_form.save()
            else:
                valid = False
        else:
            cardiac_form = None

        if valid:
            messages.success(request, f"Clinical baselines for {patient} saved successfully.")
            return redirect('patients:profile', pk=patient.pk)
    else:
        scd_form = SickleCellBaselineForm(instance=scd_baseline, prefix='scd') if show_scd else None
        dm_form = DiabetesBaselineForm(instance=dm_baseline, prefix='dm') if show_dm else None
        cardiac_form = CardiacBaselineForm(instance=cardiac_baseline, prefix='cardiac') if show_cardiac else None

    return render(request, 'clinical/baselines/baseline_forms.html', {
        'enrollment': enrollment,
        'patient': patient,
        'scd_form': scd_form,
        'dm_form': dm_form,
        'cardiac_form': cardiac_form,
        'show_scd': show_scd,
        'show_dm': show_dm,
        'show_cardiac': show_cardiac,
    })
