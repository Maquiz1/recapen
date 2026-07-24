from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from laboratory.models import LaboratoryCategory, LaboratoryType, LaboratoryTest
from laboratory.forms import CategoryForm, TypeForm

def category_list(request):
    categories = LaboratoryCategory.objects.filter(is_deleted=False).order_by('name')
    paginator = Paginator(categories, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'laboratory/category_list.html', {'categories': page_obj})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            if request.user.is_authenticated:
                category.created_by = request.user
                category.updated_by = request.user
            category.save()
            messages.success(request, f"Category '{category.name}' added successfully.")
            return redirect('laboratory:category_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm()
    return render(request, 'laboratory/category_form.html', {'form': form, 'title': 'Register New Category'})

def category_edit(request, pk):
    category = get_object_or_404(LaboratoryCategory, pk=pk, is_deleted=False)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            c = form.save(commit=False)
            if request.user.is_authenticated:
                c.updated_by = request.user
            c.save()
            messages.success(request, f"Category '{c.name}' updated successfully.")
            return redirect('laboratory:category_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'laboratory/category_form.html', {'form': form, 'title': f'Edit Category: {category.name}'})

def category_delete(request, pk):
    category = get_object_or_404(LaboratoryCategory, pk=pk, is_deleted=False)
    
    # Check if category has any active tests
    if LaboratoryTest.objects.filter(laboratory_category=category, is_deleted=False).exists():
        messages.error(request, f"Cannot delete '{category.name}' because it contains active tests.")
        return redirect('laboratory:category_list')
        
    category.is_deleted = True
    if request.user.is_authenticated:
        category.updated_by = request.user
    category.save()
    messages.success(request, f"Category '{category.name}' deleted successfully.")
    return redirect('laboratory:category_list')

def type_list(request):
    types = LaboratoryType.objects.filter(is_deleted=False).select_related('category').order_by('category__name', 'name')
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
    type_obj = get_object_or_404(LaboratoryType, pk=pk, is_deleted=False)
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
    type_obj = get_object_or_404(LaboratoryType, pk=pk, is_deleted=False)
    
    # Check if type has any active tests
    if LaboratoryTest.objects.filter(laboratory_type=type_obj, is_deleted=False).exists():
        messages.error(request, f"Cannot delete '{type_obj.name}' because it contains active tests.")
        return redirect('laboratory:type_list')
        
    type_obj.is_deleted = True
    if request.user.is_authenticated:
        type_obj.updated_by = request.user
    type_obj.save()
    messages.success(request, f"Type '{type_obj.name}' deleted successfully.")
    return redirect('laboratory:type_list')
