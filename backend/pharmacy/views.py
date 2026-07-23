from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from pharmacy.models import InventoryBatch
from medications.models import Medication
from django.db.models import Sum, F, Value
from django.db.models.functions import Coalesce

def low_stock_list(request):
    medications_with_stock = Medication.objects.annotate(
        total_stock=Sum('batches__quantity_in_stock')
    )
    meds_low = medications_with_stock.annotate(
        actual_stock=Coalesce('total_stock', Value(0))
    ).filter(actual_stock__lte=F('reorder_level'), is_active=True)

    return render(request, 'pharmacy/low_stock_list.html', {'medications': meds_low})

def expiring_soon_list(request):
    today = timezone.now().date()
    three_months_from_now = today + timedelta(days=90)
    
    batches = InventoryBatch.objects.filter(
        quantity_in_stock__gt=0,
        expiration_date__gt=today,
        expiration_date__lte=three_months_from_now
    ).order_by('expiration_date')

    return render(request, 'pharmacy/expiring_soon_list.html', {'batches': batches})

def expired_list(request):
    today = timezone.now().date()
    
    batches = InventoryBatch.objects.filter(
        quantity_in_stock__gt=0,
        expiration_date__lte=today
    ).order_by('expiration_date')

    return render(request, 'pharmacy/expired_list.html', {'batches': batches})

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from clinical.models import Prescription
from .models import Dispensation, DispensationBatch
from .forms import DispensationForm

def batch_list(request):
    batches = InventoryBatch.objects.all().order_by('-created_at')
    return render(request, 'pharmacy/batch_list.html', {'batches': batches})

def dispensation_list(request):
    dispensations = Dispensation.objects.select_related('prescription', 'prescription__patient', 'prescription__medication', 'dispensed_by').order_by('-dispensed_date')
    return render(request, 'pharmacy/dispensation_list.html', {'dispensations': dispensations})

def dispense_prescription(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)
    
    # Check if already dispensed
    if hasattr(prescription, 'dispensation') and prescription.dispensation:
        messages.warning(request, "This prescription has already been dispensed.")
        return redirect('clinical:prescription_list')
        
    medication = prescription.medication
    
    # Get total available stock for this medication
    available_batches = InventoryBatch.objects.filter(
        medication=medication, 
        quantity_in_stock__gt=0,
        expiration_date__gt=timezone.now().date()
    ).order_by('expiration_date')
    
    total_available = sum(b.quantity_in_stock for b in available_batches)
    
    if request.method == 'POST':
        form = DispensationForm(request.POST)
        if form.is_valid():
            qty_requested = form.cleaned_data['quantity_dispensed']
            
            if qty_requested > total_available:
                messages.error(request, f"Cannot dispense {qty_requested}. Only {total_available} available in stock.")
            else:
                with transaction.atomic():
                    dispensation = form.save(commit=False)
                    dispensation.prescription = prescription
                    if request.user.is_authenticated:
                        dispensation.dispensed_by = request.user
                    dispensation.save()
                    
                    # Deduct from batches
                    qty_to_deduct = qty_requested
                    for batch in available_batches:
                        if qty_to_deduct <= 0:
                            break
                        
                        take_from_batch = min(qty_to_deduct, batch.quantity_in_stock)
                        
                        # Create DispensationBatch record
                        DispensationBatch.objects.create(
                            dispensation=dispensation,
                            batch=batch,
                            quantity=take_from_batch
                        )
                        
                        batch.quantity_in_stock -= take_from_batch
                        batch.save()
                        
                        qty_to_deduct -= take_from_batch
                        
                    messages.success(request, f"Successfully dispensed {qty_requested} units of {medication.name}.")
                    return redirect('clinical:prescription_list')
    else:
        # We don't have a numeric quantity_prescribed anymore, so default to 1 if available
        default_qty = min(1, total_available) if total_available > 0 else 0
        form = DispensationForm(initial={'quantity_dispensed': default_qty})
        
    return render(request, 'pharmacy/dispense_form.html', {
        'form': form,
        'prescription': prescription,
        'total_available': total_available,
        'available_batches': available_batches
    })
