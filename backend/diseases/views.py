from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Disease
from .forms import DiseaseForm
from django.utils import timezone
from django.core.paginator import Paginator

def disease_list(request):
    diseases = Disease.objects.filter(is_deleted=False).order_by('order', 'name')
    
    paginator = Paginator(diseases, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'diseases/disease_list.html', {'diseases': page_obj})

def disease_create(request):
    if request.method == 'POST':
        form = DiseaseForm(request.POST)
        if form.is_valid():
            disease = form.save(commit=False)
            if request.user.is_authenticated:
                disease.created_by = request.user
                disease.updated_by = request.user
            disease.save()
            messages.success(request, 'Disease registered successfully.')
            return redirect('diseases:disease_list')
    else:
        form = DiseaseForm()
    return render(request, 'diseases/disease_form.html', {'form': form, 'action': 'Register'})

def disease_update(request, pk):
    disease = get_object_or_404(Disease, pk=pk, is_deleted=False)
    if request.method == 'POST':
        form = DiseaseForm(request.POST, instance=disease)
        if form.is_valid():
            disease = form.save(commit=False)
            if request.user.is_authenticated:
                disease.updated_by = request.user
            disease.save()
            messages.success(request, 'Disease updated successfully.')
            return redirect('diseases:disease_list')
    else:
        form = DiseaseForm(instance=disease)
    return render(request, 'diseases/disease_form.html', {'form': form, 'action': 'Update'})

def disease_deactivate(request, pk):
    disease = get_object_or_404(Disease, pk=pk, is_deleted=False)
    disease.is_active = not disease.is_active
    disease.save(update_fields=['is_active'])
    status = "activated" if disease.is_active else "deactivated"
    messages.success(request, f'Disease successfully {status}.')
    return redirect('diseases:disease_list')

def disease_delete(request, pk):
    disease = get_object_or_404(Disease, pk=pk, is_deleted=False)
    disease.is_deleted = True
    disease.deleted_at = timezone.now()
    disease.save(update_fields=['is_deleted', 'deleted_at'])
    messages.success(request, 'Disease deleted successfully.')
    return redirect('diseases:disease_list')
