from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from .models import Appointment
from .forms import AppointmentForm
from patients.models import Patient
from encounters.models import Encounter

def appointment_dashboard(request):
    """
    Renders the dashboard/calendar overview of appointments.
    """
    appointments = Appointment.objects.all().select_related('patient', 'doctor').order_by('scheduled_time')
    return render(request, 'appointments/appointments_dashboard.html', {'appointments': appointments})

def appointment_list(request):
    """
    Renders a tabular list of all appointments.
    """
    appointments = Appointment.objects.all().select_related('patient', 'doctor').order_by('-scheduled_time')
    return render(request, 'appointments/appointments_list.html', {'appointments': appointments})

def book_appointment(request):
    """
    Allows staff to book a new appointment.
    """
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            if request.user.is_authenticated:
                appointment.created_by = request.user
                appointment.updated_by = request.user
            appointment.save()
            messages.success(request, "Appointment scheduled successfully.")
            return redirect('appointments:success')
    else:
        form = AppointmentForm()
        
    return render(request, 'appointments/book_appointment.html', {'form': form})

def appointment_success(request):
    """
    Shows a success page after booking an appointment.
    """
    return render(request, 'appointments/appointment_success.html')

def edit_appointment(request, pk):
    """
    Edit an existing appointment.
    """
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            appointment = form.save(commit=False)
            if request.user.is_authenticated:
                appointment.updated_by = request.user
            appointment.save()
            messages.success(request, "Appointment updated successfully.")
            return redirect('appointments:list')
    else:
        form = AppointmentForm(instance=appointment)
        
    return render(request, 'appointments/edit_appointment.html', {'form': form, 'appointment': appointment})

def check_in(request, pk):
    """
    Check-in an existing appointment and auto-generate an encounter.
    """
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
        return redirect('appointments:dashboard')
    
    # Should not GET this view, redirect back
    return redirect('appointments:dashboard')
