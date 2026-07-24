from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from diagnostics.models import DiagnosticGroup, DiagnosticCategory, DiagnosticTest
from laboratory.forms import CategoryForm, TypeForm

def category_list(request):
    categories = DiagnosticGroup.objects.filter(is_deleted=False, department__name='laboratory').order_by('name')
    paginator = Paginator(categories, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'laboratory/category_list.html', {'categories': page_obj})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            from departments.models import Department
            dept, _ = Department.objects.get_or_create(name='laboratory')
            category.department = dept
            if request.user.is_authenticated:
                category.created_by = request.user
                category.updated_by = request.user
            category.save()
            messages.success(request, f"Category '{category.name}' created successfully.")
            return redirect('laboratory:category_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm()
    return render(request, 'laboratory/category_form.html', {'form': form, 'title': 'Add Laboratory Category'})

def category_edit(request, pk):
    category = get_object_or_404(DiagnosticGroup, pk=pk, department__name='laboratory')
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f"Category '{category.name}' updated successfully.")
            return redirect('laboratory:category_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'laboratory/category_form.html', {'form': form, 'title': 'Edit Laboratory Category', 'category': category})

def category_delete(request, pk):
    category = get_object_or_404(DiagnosticGroup, pk=pk, is_deleted=False, department__name='laboratory')
    
    # Check if category is used in tests
    if DiagnosticTest.objects.filter(diagnostic_group=category, is_deleted=False).exists():
        messages.error(request, f"Cannot delete category '{category.name}' because it contains active tests. Please delete or reassign the tests first.")
        return redirect('laboratory:category_list')
        
    category.is_deleted = True
    category.save()
    messages.success(request, f"Category '{category.name}' deleted successfully.")
    return redirect('laboratory:category_list')

def category_activate(request, pk):
    category = get_object_or_404(DiagnosticGroup, pk=pk, is_deleted=False, department__name='laboratory')
    category.is_active = True
    category.save(update_fields=['is_active'])
    messages.success(request, f"Category '{category.name}' activated successfully.")
    return redirect('laboratory:category_list')

def category_deactivate(request, pk):
    category = get_object_or_404(DiagnosticGroup, pk=pk, is_deleted=False, department__name='laboratory')
    category.is_active = False
    category.save(update_fields=['is_active'])
    messages.success(request, f"Category '{category.name}' deactivated successfully.")
    return redirect('laboratory:category_list')

def type_list(request):
    types = DiagnosticCategory.objects.filter(is_deleted=False, group__department__name='laboratory').select_related('group').order_by('group__name', 'name')

    paginator = Paginator(types, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'laboratory/type_list.html', {'types': page_obj})

def type_create(request):
    if request.method == 'POST':
        form = TypeForm(request.POST)
        if form.is_valid():
            type_obj = form.save(commit=False)
            if request.user.is_authenticated:
                type_obj.created_by = request.user
                type_obj.updated_by = request.user
            type_obj.save()
            messages.success(request, f"Type '{type_obj.name}' added successfully.")
            return redirect('laboratory:type_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TypeForm()
    return render(request, 'laboratory/type_form.html', {'form': form, 'title': 'Register New Type'})

def type_edit(request, pk):
    type_obj = get_object_or_404(DiagnosticCategory, pk=pk, is_deleted=False)
    if request.method == 'POST':
        form = TypeForm(request.POST, instance=type_obj)
        if form.is_valid():
            t = form.save(commit=False)
            if request.user.is_authenticated:
                t.updated_by = request.user
            t.save()
            messages.success(request, f"Type '{t.name}' updated successfully.")
            return redirect('laboratory:type_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TypeForm(instance=type_obj)
    return render(request, 'laboratory/type_form.html', {'form': form, 'title': f'Edit Type: {type_obj.name}'})

def type_delete(request, pk):
    type_obj = get_object_or_404(DiagnosticCategory, pk=pk, is_deleted=False)
    
    # Check if type has any active tests
    if DiagnosticTest.objects.filter(diagnostic_category=type_obj, is_deleted=False).exists():
        messages.error(request, f"Cannot delete '{type_obj.name}' because it contains active tests.")
        return redirect('laboratory:type_list')
        
    type_obj.is_deleted = True
    if request.user.is_authenticated:
        type_obj.updated_by = request.user
    type_obj.save()
    messages.success(request, f"Type '{type_obj.name}' deleted successfully.")
    return redirect('laboratory:type_list')

def type_activate(request, pk):
    type_obj = get_object_or_404(DiagnosticCategory, pk=pk, is_deleted=False)
    type_obj.is_active = True
    type_obj.save(update_fields=['is_active'])
    messages.success(request, f"Type '{type_obj.name}' activated successfully.")
    return redirect('laboratory:type_list')

def type_deactivate(request, pk):
    type_obj = get_object_or_404(DiagnosticCategory, pk=pk, is_deleted=False)
    type_obj.is_active = False
    type_obj.save(update_fields=['is_active'])
    messages.success(request, f"Type '{type_obj.name}' deactivated successfully.")
    return redirect('laboratory:type_list')
