from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Medication
from .forms import MedicationForm, InventoryUpdateForm

def inventory_list(request):
    medications = Medication.objects.all().order_by('name')
    return render(request, 'medications/inventory_list.html', {'medications': medications})

def update_inventory(request, pk):
    medication = get_object_or_404(Medication, pk=pk)
    
    if request.method == 'POST':
        form = InventoryUpdateForm(request.POST, instance=medication)
        if form.is_valid():
            form.save()
            messages.success(request, f"Inventory updated for {medication.name}.")
            return redirect('medications:inventory_list')
    else:
        form = InventoryUpdateForm(instance=medication)
        
    return render(request, 'medications/update_inventory.html', {
        'form': form,
        'medication': medication
    })
