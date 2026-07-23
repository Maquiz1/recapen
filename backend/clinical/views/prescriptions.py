from django.shortcuts import render
from clinical.models import Prescription

def prescription_list(request):
    prescriptions = Prescription.objects.select_related('patient', 'medication', 'encounter').order_by('-created_at')
    return render(request, 'clinical/prescription_list.html', {'prescriptions': prescriptions})
