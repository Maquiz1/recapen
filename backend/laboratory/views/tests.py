from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from laboratory.models import LaboratoryTest
from laboratory.forms import LabTestForm
from django.core.paginator import Paginator

def test_list(request):
    tests = LaboratoryTest.objects.filter(is_deleted=False).order_by('laboratory_category__name', 'laboratory_type__name', 'name')
    paginator = Paginator(tests, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'laboratory/test_list.html', {'tests': page_obj})

def test_create(request):
    if request.method == 'POST':
        form = LabTestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            if request.user.is_authenticated:
                test.created_by = request.user
                test.updated_by = request.user
            test.save()
            messages.success(request, f"Laboratory test '{test.name}' registered successfully.")
            return redirect('laboratory:list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LabTestForm()
    return render(request, 'laboratory/test_form.html', {'form': form, 'title': 'Register New Test'})

def test_edit(request, pk):
    test = get_object_or_404(LaboratoryTest, pk=pk, is_deleted=False)
    if request.method == 'POST':
        form = LabTestForm(request.POST, instance=test)
        if form.is_valid():
            t = form.save(commit=False)
            if request.user.is_authenticated:
                t.updated_by = request.user
            t.save()
            messages.success(request, f"Laboratory test '{t.name}' updated successfully.")
            return redirect('laboratory:list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LabTestForm(instance=test)
    return render(request, 'laboratory/test_form.html', {'form': form, 'title': f'Edit Test: {test.name}'})

def test_activate(request, pk):
    test = get_object_or_404(LaboratoryTest, pk=pk, is_deleted=False)
    test.is_active = True
    test.save()
    messages.success(request, f'Test "{test.name}" activated successfully.')
    return redirect('laboratory:list')

def test_deactivate(request, pk):
    test = get_object_or_404(LaboratoryTest, pk=pk, is_deleted=False)
    test.is_active = False
    test.save()
    messages.warning(request, f'Test "{test.name}" deactivated.')
    return redirect('laboratory:list')

def test_delete(request, pk):
    test = get_object_or_404(LaboratoryTest, pk=pk, is_deleted=False)
    test.is_deleted = True
    test.save()
    messages.error(request, f'Test "{test.name}" deleted.')
    return redirect('laboratory:list')

def test_edit_redirect(request):
    first_test = LaboratoryTest.objects.filter(is_deleted=False).first()
    if first_test:
        return redirect('laboratory:edit', pk=first_test.pk)
    messages.warning(request, "No lab tests registered yet. Please create a lab test first.")
    return redirect('laboratory:list')
