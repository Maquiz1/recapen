from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Appointment
from .forms import AppointmentForm
from patients.models import Patient
from encounters.models import Encounter

def daily_calendar(request):
    # Default to today
    today = timezone.now().date()
    # In a real app, you might filter by the requested date via query params.
    appointments = Appointment.objects.filter(scheduled_time__date=today).select_related('patient', 'doctor')
    return render(request, 'appointments/calendar.html', {'appointments': appointments, 'date': today})

def book_appointment(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id, is_deleted=False)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            if request.user.is_authenticated:
                appointment.created_by = request.user
                appointment.updated_by = request.user
            appointment.save()
            messages.success(request, "Appointment scheduled successfully.")
            return redirect('patients:profile', pk=patient.pk)
    else:
        form = AppointmentForm()
        
    return render(request, 'appointments/book.html', {'form': form, 'patient': patient})

def check_in(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    
    if request.method == 'POST':
        if appointment.status == 'scheduled':
            appointment.status = 'arrived'
            
            # Auto-generate Encounter
            encounter = Encounter.objects.create(
                patient=appointment.patient,
                doctor=appointment.doctor,
                status='in_progress',
                encounter_type='followup',
                created_by=request.user if request.user.is_authenticated else None,
                updated_by=request.user if request.user.is_authenticated else None
            )
            
            appointment.encounter = encounter
            appointment.save()
            
            messages.success(request, f"{appointment.patient} has been checked in. An encounter was automatically created.")
        return redirect('appointments:calendar')
    
    # Should not GET this view, redirect back
    return redirect('appointments:calendar')
