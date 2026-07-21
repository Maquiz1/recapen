from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import ClinicalForm, FollowUpRule

from django.apps import apps

def form_has_data_for_rule(rule, form):
    relation_map = {
        'vitals': 'vitals',
        'vt': 'vitals',
        'hospitalization': 'hospitalization',
        'hosp': 'hospitalization',
        'risk': 'risk',
        'risks': 'risk',
        'socioeconomic': 'socioeconomic',
        'se': 'socioeconomic',
        'treatment': 'treatment',
        'tx': 'treatment',
        'history': 'history',
        'hist': 'history',
        'symptom': 'symptom',
        'symptoms': 'symptom',
        'symp': 'symptom',
        'complications': 'complications',
        'comp': 'complications',
        'school_home_assessment': 'school_home_assessment',
        'schoolhomeassessment': 'school_home_assessment',
        'schoolhome': 'school_home_assessment'
    }
    
    relation_name = relation_map.get(form.code.lower())
    if not relation_name:
        return False
        
    from encounters.models import Encounter
    
    query_kwargs = {
        'patient__enrollment__cohort__iexact': rule.cohort,
        'encounter_type': rule.encounter_type,
        'visit_nature': rule.visit_nature,
    }
    query_kwargs[f"{relation_name}__isnull"] = False
    
    return Encounter.objects.filter(**query_kwargs).exists()

def config_dashboard(request):
    # Auto-sync models from clinical app to ClinicalForm registry
    try:
        clinical_config = apps.get_app_config('clinical')
        valid_codes = []
        for model in clinical_config.get_models():
            if model._meta.object_name.startswith('Historical') or model._meta.proxy:
                continue
            code = model._meta.model_name
            valid_codes.append(code)
            
            # Create or update name
            ClinicalForm.objects.get_or_create(
                code=code,
                defaults={
                    'name': model._meta.verbose_name.title(),
                    'description': f"Form data model for {model._meta.verbose_name.title()}."
                }
            )
        # Clean up obsolete database entries
        ClinicalForm.objects.exclude(code__in=valid_codes).delete()
    except LookupError:
        pass

    rules = list(FollowUpRule.objects.all().prefetch_related('required_forms'))
    
    # Sort for the regular table (which we will still keep or replace with pivot)
    rules.sort(key=lambda r: (r.get_cohort_display(), r.get_encounter_type_display(), r.get_visit_nature_display()))
    
    cohort_choices = [
        ('cardiac', 'Cardiac'),
        ('scd', 'SCD'),
        ('dm', 'DM'),
    ]
    encounter_types = [
        ('initial', 'Baseline'),
        ('followup', 'Follow-up'),
        ('routine', 'Routine Checkup'),
        ('emergency', 'Emergency'),
    ]
    visit_natures = [
        ('scheduled', 'Scheduled'),
        ('unscheduled', 'Unscheduled'),
    ]
    
    columns = []
    for et_code, et_name in encounter_types:
        for vn_code, vn_name in visit_natures:
            columns.append({
                'et_code': et_code,
                'vn_code': vn_code,
                'label': f"{et_name} ({vn_name})"
            })
            
    pivot_rows = []
    for cohort_code, cohort_name in cohort_choices:
        row_cells = []
        for col in columns:
            rule = next((r for r in rules if r.cohort == cohort_code and r.encounter_type == col['et_code'] and r.visit_nature == col['vn_code']), None)
            
            forms_data = []
            has_any_data = False
            if rule:
                for form in rule.required_forms.all().order_by('name'):
                    has_data = form_has_data_for_rule(rule, form)
                    if has_data:
                        has_any_data = True
                    forms_data.append({
                        'form': form,
                        'has_data': has_data
                    })
            
            row_cells.append({
                'column': col,
                'rule': rule,
                'forms_data': forms_data,
                'has_any_data': has_any_data
            })
        pivot_rows.append({
            'cohort_code': cohort_code,
            'cohort_name': cohort_name,
            'cells': row_cells
        })
        
    forms = ClinicalForm.objects.all()
    
    return render(request, 'study_config/dashboard.html', {
        'rules': rules,
        'forms': forms,
        'columns': columns,
        'pivot_rows': pivot_rows,
    })

def manage_forms(request):
    # Auto-sync models from clinical app to ClinicalForm registry
    try:
        clinical_config = apps.get_app_config('clinical')
        valid_codes = []
        for model in clinical_config.get_models():
            if model._meta.object_name.startswith('Historical') or model._meta.proxy:
                continue
            code = model._meta.model_name
            valid_codes.append(code)
            
            ClinicalForm.objects.get_or_create(
                code=code,
                defaults={
                    'name': model._meta.verbose_name.title(),
                    'description': f"Form data model for {model._meta.verbose_name.title()}."
                }
            )
        # Clean up obsolete database entries
        ClinicalForm.objects.exclude(code__in=valid_codes).delete()
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
        cohorts = request.POST.getlist('cohorts')
        encounter_types = request.POST.getlist('encounter_types')
        visit_natures = request.POST.getlist('visit_natures')
        form_ids = request.POST.getlist('forms')
        
        if cohorts and encounter_types and visit_natures:
            count = 0
            for cohort in cohorts:
                for et in encounter_types:
                    for vn in visit_natures:
                        # Get or create rule
                        rule, created = FollowUpRule.objects.get_or_create(
                            cohort=cohort,
                            encounter_type=et,
                            visit_nature=vn
                        )
                        # Update forms by appending
                        rule.required_forms.add(*form_ids)
                        count += 1
            messages.success(request, f"Successfully updated {count} mapping rules.")
            
        return redirect('study_config:dashboard')

def remove_form_from_rule(request, rule_id, form_id):
    rule = get_object_or_404(FollowUpRule, pk=rule_id)
    form = get_object_or_404(ClinicalForm, pk=form_id)
    
    if form_has_data_for_rule(rule, form):
        messages.error(request, f"Cannot remove form '{form.name}' because patient data has already been recorded under this rule.")
        return redirect('study_config:dashboard')
        
    rule.required_forms.remove(form)
    messages.success(request, f"Removed form '{form.name}' from rule.")
    return redirect('study_config:dashboard')

def delete_rule(request, rule_id):
    rule = get_object_or_404(FollowUpRule, pk=rule_id)
    
    # Check if any associated form has data
    for form in rule.required_forms.all():
        if form_has_data_for_rule(rule, form):
            messages.error(request, f"Cannot delete this rule because form '{form.name}' already has patient records submitted under this rule.")
            return redirect('study_config:dashboard')
            
    rule.delete()
    messages.success(request, "Mapping rule deleted successfully.")
    return redirect('study_config:dashboard')
