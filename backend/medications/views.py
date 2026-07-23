from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Medication
from .forms import MedicationForm, InventoryUpdateForm

def inventory_list(request):
    medications = Medication.objects.all().order_by('name')
    return render(request, 'medications/inventory_list.html', {'medications': medications})


def create_medication(request):
    if request.method == 'POST':
        form = MedicationForm(request.POST)
        if form.is_valid():
            med = form.save()
            messages.success(request, f"Medication '{med.name}' added successfully.")
            return redirect('medications:inventory_list')
    else:
        form = MedicationForm()
        
    return render(request, 'medications/medication_form.html', {'form': form, 'is_edit': False})

def edit_medication(request, pk):
    medication = get_object_or_404(Medication, pk=pk)
    
    if request.method == 'POST':
        form = MedicationForm(request.POST, instance=medication)
        if form.is_valid():
            form.save()
            messages.success(request, f"Medication '{medication.name}' updated successfully.")
            return redirect('medications:inventory_list')
    else:
        form = MedicationForm(instance=medication)
        
    return render(request, 'medications/medication_form.html', {'form': form, 'is_edit': True})
