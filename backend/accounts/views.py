from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import CustomUser
from .forms import DoctorCreationForm, DoctorEditForm
from patients.models import Patient

def doctor_list_grid(request):
    doctors = CustomUser.objects.filter(is_active=True).order_by('last_name', 'first_name')
    return render(request, 'accounts/doctors_grid.html', {'doctors': doctors})

def doctor_list_cards(request):
    doctors = CustomUser.objects.filter(is_active=True).order_by('last_name', 'first_name')
    return render(request, 'accounts/doctors_cards.html', {'doctors': doctors})

def doctor_create(request):
    if request.method == 'POST':
        form = DoctorCreationForm(request.POST)
        if form.is_valid():
            doctor = form.save()
            messages.success(request, f"Doctor '{doctor.username}' added successfully.")
            return redirect('accounts:grid')
    else:
        form = DoctorCreationForm()
    return render(request, 'accounts/doctor_form.html', {'form': form, 'title': 'Add Doctor'})

def doctor_edit(request, pk):
    doctor = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = DoctorEditForm(request.POST, instance=doctor)
        if form.is_valid():
            doctor = form.save()
            messages.success(request, f"Doctor '{doctor.username}' details updated.")
            return redirect('accounts:grid')
    else:
        form = DoctorEditForm(instance=doctor)
    return render(request, 'accounts/doctor_form.html', {'form': form, 'title': 'Edit Doctor Details', 'doctor': doctor})

def doctor_edit_redirect(request):
    first_doctor = CustomUser.objects.filter(is_active=True).first()
    if first_doctor:
        return redirect('accounts:edit', pk=first_doctor.pk)
    messages.warning(request, "No doctors registered yet. Please add a doctor first.")
    return redirect('accounts:grid')

def doctor_profile(request, pk):
    doctor = get_object_or_404(CustomUser, pk=pk)
    # Simple count of patients registered/created by this doctor
    patients_count = Patient.objects.filter(created_by=doctor, is_deleted=False).count()
    return render(request, 'accounts/doctors_profile.html', {
        'doctor': doctor,
        'patients_count': patients_count
    })

def doctor_profile_redirect(request):
    first_doctor = CustomUser.objects.filter(is_active=True).first()
    if first_doctor:
        return redirect('accounts:profile', pk=first_doctor.pk)
    messages.warning(request, "No doctors registered yet. Please add a doctor first.")
    return redirect('accounts:grid')

def doctor_dashboard(request, pk):
    doctor = get_object_or_404(CustomUser, pk=pk)
    
    # Metrics
    total_registered = Patient.objects.filter(created_by=doctor, is_deleted=False).count()
    active_cohort = Patient.objects.filter(created_by=doctor, status='enrolled', is_deleted=False).count()
    inactive_cohort = Patient.objects.filter(created_by=doctor, is_deleted=False).exclude(status='enrolled').count()

    return render(request, 'accounts/doctor_dashboard.html', {
        'doctor': doctor,
        'total_registered': total_registered,
        'active_cohort': active_cohort,
        'inactive_cohort': inactive_cohort,
    })

def doctor_dashboard_redirect(request):
    first_doctor = CustomUser.objects.filter(is_active=True).first()
    if first_doctor:
        return redirect('accounts:dashboard', pk=first_doctor.pk)
    messages.warning(request, "No doctors registered yet. Please add a doctor first.")
    return redirect('accounts:grid')
