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

from django.contrib.admin.views.decorators import staff_member_required
from .forms import StaffSignupForm

@staff_member_required
def register_staff(request):
    if request.method == 'POST':
        form = StaffSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            messages.success(request, f"Staff account for {user.username} created successfully.")
            return redirect('admin')
    else:
        form = StaffSignupForm()
    return render(request, 'registration/signup.html', {'form': form})

from .forms import StaffCreationForm, StaffEditForm

@staff_member_required
def staff_list(request):
    staff_members = CustomUser.objects.filter(is_active=True).order_by('last_name', 'first_name')
    return render(request, 'accounts/staff_list.html', {'staff_members': staff_members})

@staff_member_required
def staff_create(request):
    if request.method == 'POST':
        form = StaffCreationForm(request.POST)
        if form.is_valid():
            staff = form.save()
            messages.success(request, f"Staff '{staff.username}' added successfully.")
            return redirect('accounts:staff_list')
    else:
        form = StaffCreationForm()
    return render(request, 'accounts/staff_form.html', {'form': form, 'title': 'Add Staff Member'})

@staff_member_required
def staff_edit(request, pk):
    staff = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = StaffEditForm(request.POST, instance=staff)
        if form.is_valid():
            staff = form.save()
            messages.success(request, f"Staff '{staff.username}' details updated.")
            return redirect('accounts:staff_list')
    else:
        form = StaffEditForm(instance=staff)
    return render(request, 'accounts/staff_form.html', {'form': form, 'title': 'Edit Staff Member', 'staff': staff})

@staff_member_required
def staff_deactivate(request, pk):
    staff = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        staff.is_active = False
        staff.save()
        messages.success(request, f"Staff member '{staff.username}' has been deactivated.")
    return redirect('accounts:staff_list')


from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('accounts:profile_edit')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'accounts/profile_edit.html', {'form': form, 'title': 'My Profile'})
