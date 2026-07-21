from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import ClinicalForm, FollowUpRule

from django.apps import apps

def config_dashboard(request):
    # Auto-sync models from clinical app to ClinicalForm registry
    try:
        clinical_config = apps.get_app_config('clinical')
        for model in clinical_config.get_models():
            if model._meta.object_name.startswith('Historical') or model._meta.proxy:
                continue
            code = model._meta.model_name
            name = model._meta.verbose_name.title()
            
            # Create or update name
            ClinicalForm.objects.get_or_create(
                code=code,
                defaults={
                    'name': name,
                    'description': f"Form data model for {name}."
                }
            )
    except LookupError:
        pass

    rules = FollowUpRule.objects.all().prefetch_related('required_forms')
    forms = ClinicalForm.objects.all()
    
    return render(request, 'study_config/dashboard.html', {
        'rules': rules,
        'forms': forms,
    })

def manage_forms(request):
    # Auto-sync models from clinical app to ClinicalForm registry
    try:
        clinical_config = apps.get_app_config('clinical')
        for model in clinical_config.get_models():
            if model._meta.object_name.startswith('Historical') or model._meta.proxy:
                continue
            code = model._meta.model_name
            name = model._meta.verbose_name.title()
            ClinicalForm.objects.get_or_create(
                code=code,
                defaults={
                    'name': name,
                    'description': f"Form data model for {name}."
                }
            )
    except LookupError:
        pass

    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        desc = request.POST.get('description')
        if name and code:
            ClinicalForm.objects.create(name=name, code=code, description=desc)
            messages.success(request, f"Form '{name}' created successfully.")
        return redirect('study_config:manage_forms')
        
    forms = ClinicalForm.objects.all()
    return render(request, 'study_config/manage_forms.html', {'forms': forms})

def manage_rules(request):
    if request.method == 'POST':
        cohort = request.POST.get('cohort')
        visit_nature = request.POST.get('visit_nature')
        form_ids = request.POST.getlist('forms')
        
        if cohort and visit_nature:
            # Get or create rule
            rule, created = FollowUpRule.objects.get_or_create(
                cohort=cohort,
                visit_nature=visit_nature
            )
            # Update forms
            rule.required_forms.set(form_ids)
            messages.success(request, f"Rule for {rule} updated successfully.")
            
        return redirect('study_config:dashboard')
