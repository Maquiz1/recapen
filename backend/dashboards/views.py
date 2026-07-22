from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from patients.models import Enrollment

@login_required
def admin(request):
    enrollments = Enrollment.objects.select_related('patient').order_by('-created_at')[:10]
    patients_count = Enrollment.objects.count()
    return render(request, 'dashboards/admin.html', {
        'enrollments': enrollments,
        'patients_count': patients_count
    })

@login_required
def medical(request):
    return render(request, 'dashboards/medical.html')

@login_required
def clinic(request):
    return render(request, 'dashboards/clinic.html')
