from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Department
from .forms import DepartmentForm

@staff_member_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'departments/department_list.html', {'departments': departments})

@staff_member_required
def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            dept = form.save(commit=False)
            dept.created_by = request.user
            dept.save()
            messages.success(request, f"Department '{dept.name}' created successfully.")
            return redirect('departments:list')
    else:
        form = DepartmentForm(initial={'is_active': True})
    return render(request, 'departments/department_form.html', {'form': form, 'title': 'Add Department'})

@staff_member_required
def department_edit(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            dept = form.save(commit=False)
            dept.updated_by = request.user
            dept.save()
            messages.success(request, f"Department '{dept.name}' updated successfully.")
            return redirect('departments:list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'departments/department_form.html', {'form': form, 'title': 'Edit Department', 'department': department})

@staff_member_required
def department_deactivate(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.is_active = False
        department.save()
        messages.success(request, f"Department '{department.name}' has been deactivated.")
    return redirect('departments:list')
