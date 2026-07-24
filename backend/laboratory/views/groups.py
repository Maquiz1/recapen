from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from diagnostics.models import DiagnosticGroup, DiagnosticCategory, DiagnosticTest
from laboratory.forms import GroupForm, GroupForm

def group_list(request):
    groups = DiagnosticGroup.objects.filter(is_deleted=False, department__name='laboratory').order_by('name')
    paginator = Paginator(groups, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'laboratory/group_list.html', {'groups': page_obj})

def group_create(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            from departments.models import Department
            dept, _ = Department.objects.get_or_create(name='laboratory')
            group.department = dept
            if request.user.is_authenticated:
                group.created_by = request.user
                group.updated_by = request.user
            group.save()
            messages.success(request, f"Group '{group.name}' created successfully.")
            return redirect('laboratory:group_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = GroupForm()
    return render(request, 'laboratory/category_form.html', {'form': form, 'title': 'Add Laboratory Category'})

def group_edit(request, pk):
    category = get_object_or_404(DiagnosticGroup, pk=pk, department__name='laboratory')
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f"Group '{group.name}' updated successfully.")
            return redirect('laboratory:group_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = GroupForm(instance=category)
    return render(request, 'laboratory/category_form.html', {'form': form, 'title': 'Edit Laboratory Category', 'category': category})

def group_delete(request, pk):
    category = get_object_or_404(DiagnosticGroup, pk=pk, is_deleted=False, department__name='laboratory')
    
    # Check if category is used in tests
    if DiagnosticTest.objects.filter(diagnostic_group=category, is_deleted=False).exists():
        messages.error(request, f"Cannot delete category '{group.name}' because it contains active tests. Please delete or reassign the tests first.")
        return redirect('laboratory:group_list')
        
    group.is_deleted = True
    group.save()
    messages.success(request, f"Group '{group.name}' deleted successfully.")
    return redirect('laboratory:group_list')

def group_activate(request, pk):
    category = get_object_or_404(DiagnosticGroup, pk=pk, is_deleted=False, department__name='laboratory')
    group.is_active = True
    group.save(update_fields=['is_active'])
    messages.success(request, f"Group '{group.name}' activated successfully.")
    return redirect('laboratory:group_list')

def group_deactivate(request, pk):
    category = get_object_or_404(DiagnosticGroup, pk=pk, is_deleted=False, department__name='laboratory')
    group.is_active = False
    group.save(update_fields=['is_active'])
    messages.success(request, f"Group '{group.name}' deactivated successfully.")
    return redirect('laboratory:group_list')

def category_list(request):
    categories = DiagnosticCategory.objects.filter(is_deleted=False, group__department__name='laboratory').select_related('group').order_by('group__name', 'name')

    paginator = Paginator(groups, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'laboratory/group_list.html', {'categories': page_obj})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            type_obj = form.save(commit=False)
            if request.user.is_authenticated:
                group.created_by = request.user
                group.updated_by = request.user
            group.save()
            messages.success(request, f"Category '{group.name}' added successfully.")
            return redirect('laboratory:category_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm()
    return render(request, 'laboratory/type_form.html', {'form': form, 'title': 'Register New Type'})

def category_edit(request, pk):
    type_obj = get_object_or_404(DiagnosticCategory, pk=pk, is_deleted=False)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=type_obj)
        if form.is_valid():
            t = form.save(commit=False)
            if request.user.is_authenticated:
                t.updated_by = request.user
            t.save()
            messages.success(request, f"Category '{t.name}' updated successfully.")
            return redirect('laboratory:category_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm(instance=type_obj)
    return render(request, 'laboratory/type_form.html', {'form': form, 'title': f'Edit Type: {group.name}'})

def category_delete(request, pk):
    type_obj = get_object_or_404(DiagnosticCategory, pk=pk, is_deleted=False)
    
    # Check if type has any active tests
    if DiagnosticTest.objects.filter(diagnostic_group=type_obj, is_deleted=False).exists():
        messages.error(request, f"Cannot delete '{group.name}' because it contains active tests.")
        return redirect('laboratory:category_list')
        
    group.is_deleted = True
    if request.user.is_authenticated:
        group.updated_by = request.user
    group.save()
    messages.success(request, f"Category '{group.name}' deleted successfully.")
    return redirect('laboratory:category_list')

def category_activate(request, pk):
    type_obj = get_object_or_404(DiagnosticCategory, pk=pk, is_deleted=False)
    group.is_active = True
    group.save(update_fields=['is_active'])
    messages.success(request, f"Category '{group.name}' activated successfully.")
    return redirect('laboratory:category_list')

def category_deactivate(request, pk):
    type_obj = get_object_or_404(DiagnosticCategory, pk=pk, is_deleted=False)
    group.is_active = False
    group.save(update_fields=['is_active'])
    messages.success(request, f"Category '{group.name}' deactivated successfully.")
    return redirect('laboratory:category_list')
