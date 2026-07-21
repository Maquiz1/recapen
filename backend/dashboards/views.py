from django.shortcuts import render

from patients.models import Enrollment

def admin(request):
    enrollments = Enrollment.objects.select_related('patient').order_by('-created_at')[:10]
    patients_count = Enrollment.objects.count()
    return render(request, 'dashboards/admin.html', {
        'enrollments': enrollments,
        'patients_count': patients_count
    })

def medical(request):
    return render(request, 'dashboards/medical.html')

def clinic(request):
    return render(request, 'dashboards/clinic.html')
