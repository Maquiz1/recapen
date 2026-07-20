from django.shortcuts import render

def admin(request):
    return render(request, 'dashboards/admin.html')

def medical(request):
    return render(request, 'dashboards/medical.html')

def clinic(request):
    return render(request, 'dashboards/clinic.html')
