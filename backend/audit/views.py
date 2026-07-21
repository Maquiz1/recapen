from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from patients.models import Patient
from encounters.models import Encounter
from orders.models import Order
from medications.models import Medication
from itertools import chain
from operator import attrgetter

def audit_dashboard(request):
    # Get recent history across all tracked models
    # We take the latest 50 records from each and then sort them in Python
    patient_history = list(Patient.history.all()[:50])
    encounter_history = list(Encounter.history.all()[:50])
    order_history = list(Order.history.all()[:50])
    medication_history = list(Medication.history.all()[:50])
    
    # Combine and sort by history_date descending
    all_history = sorted(
        chain(patient_history, encounter_history, order_history, medication_history),
        key=attrgetter('history_date'),
        reverse=True
    )[:100] # keep top 100 recent
    
    return render(request, 'audit/dashboard.html', {
        'history_records': all_history,
        'title': 'System Audit Trail'
    })

def patient_history(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    # Get all history records for this specific patient
    history_records = patient.history.all()
    
    return render(request, 'audit/patient_history.html', {
        'patient': patient,
        'history_records': history_records,
        'title': f'Audit Trail: {patient}'
    })
