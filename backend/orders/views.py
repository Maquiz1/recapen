from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from patients.models import Patient
from encounters.models import Encounter
from .models import Order
from .forms import PrescriptionForm

def prescribe_medication(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id, is_deleted=False)
    
    # We need an active encounter to attach the order to. 
    # If one doesn't exist, we'll create a dummy one or fail. 
    # For now, get or create the in_progress encounter.
    encounter, created = Encounter.objects.get_or_create(
        patient=patient,
        status='in_progress',
        defaults={
            'doctor': request.user if request.user.is_authenticated else None,
            'encounter_type': 'followup'
        }
    )
    
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.patient = patient
            order.encounter = encounter
            order.order_type = 'pharmacy'
            order.status = 'pending'
            if request.user.is_authenticated:
                order.ordering_doctor = request.user
                order.created_by = request.user
                order.updated_by = request.user
            order.save()
            
            messages.success(request, f"Prescription for {order.medication.name} generated successfully.")
            return redirect('patients:profile', pk=patient.pk)
    else:
        form = PrescriptionForm()
        
    return render(request, 'orders/prescribe_medication.html', {
        'form': form,
        'patient': patient
    })
