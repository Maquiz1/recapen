from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from orders.models import Order
from .forms import DispensationForm
from .models import Dispensation
from django.db import transaction

def pending_prescriptions(request):
    orders = Order.objects.filter(order_type='pharmacy', status='pending').select_related('patient', 'medication', 'ordering_doctor').order_by('order_date')
    return render(request, 'pharmacy/pending_prescriptions.html', {'orders': orders})

def fulfill_prescription(request, pk):
    order = get_object_or_404(Order, pk=pk, order_type='pharmacy')
    
    if request.method == 'POST':
        form = DispensationForm(request.POST)
        if form.is_valid():
            dispensation = form.save(commit=False)
            dispensation.order = order
            if request.user.is_authenticated:
                dispensation.dispensed_by = request.user
                dispensation.created_by = request.user
                dispensation.updated_by = request.user
                
            medication = order.medication
            
            # Simple inventory check
            if medication.stock_quantity < dispensation.quantity_dispensed:
                messages.error(request, f"Cannot dispense {dispensation.quantity_dispensed}. Only {medication.stock_quantity} in stock.")
            else:
                with transaction.atomic():
                    # Deduct stock
                    medication.stock_quantity -= dispensation.quantity_dispensed
                    medication.save()
                    
                    # Save dispensation
                    dispensation.save()
                    
                    # Complete order
                    order.status = 'completed'
                    order.save()
                
                messages.success(request, f"Dispensed {dispensation.quantity_dispensed} of {medication.name} for {order.patient}.")
                return redirect('pharmacy:pending_prescriptions')
    else:
        form = DispensationForm()
        
    return render(request, 'pharmacy/fulfill_prescription.html', {
        'form': form,
        'order': order
    })
