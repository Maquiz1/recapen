from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from patients.models import Patient
from encounters.models import Encounter
from .models import Order
from .forms import PrescriptionForm, OrderLabTestForm

def order_lab_test(request, encounter_id):
    encounter = get_object_or_404(Encounter, pk=encounter_id)
    patient = encounter.patient

    if request.method == 'POST':
        form = OrderLabTestForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.patient = patient
            order.encounter = encounter
            order.order_type = 'lab'
            order.status = 'pending'
            if request.user.is_authenticated:
                order.ordering_doctor = request.user
                order.created_by = request.user
                order.updated_by = request.user
            order.save()

            messages.success(request, f"Lab test '{order.test.name}' ordered successfully.")
            return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
    else:
        form = OrderLabTestForm()

    return render(request, 'orders/order_lab_test.html', {
        'form': form,
        'patient': patient,
        'encounter': encounter
    })

def prescribe_medication(request, encounter_id):
    encounter = get_object_or_404(Encounter, pk=encounter_id)
    patient = encounter.patient

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
            return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
    else:
        form = PrescriptionForm()

    return render(request, 'orders/prescribe_medication.html', {
        'form': form,
        'patient': patient,
        'encounter': encounter
    })
