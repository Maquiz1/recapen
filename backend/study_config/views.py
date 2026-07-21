from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import ClinicalForm, FollowUpRule

def config_dashboard(request):
    rules = FollowUpRule.objects.all().prefetch_related('required_forms')
    forms = ClinicalForm.objects.all()
    
    return render(request, 'study_config/dashboard.html', {
        'rules': rules,
        'forms': forms,
    })

def manage_forms(request):
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
