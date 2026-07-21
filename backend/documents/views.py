from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import PatientDocument
from .forms import DocumentUploadForm
from patients.models import Patient

def upload_document(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id, is_deleted=False)
    
    if request.method == 'POST':
        # Notice we pass request.FILES because this form handles file uploads
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.patient = patient
            if request.user.is_authenticated:
                document.uploaded_by = request.user
                document.created_by = request.user
                document.updated_by = request.user
            document.save()
            messages.success(request, f"Document uploaded successfully for {patient}.")
            return redirect('patients:profile', pk=patient.pk)
    else:
        form = DocumentUploadForm()
        
    return render(request, 'documents/upload.html', {'form': form, 'patient': patient})

def delete_document(request, pk):
    document = get_object_or_404(PatientDocument, pk=pk)
    patient_pk = document.patient.pk
    
    if request.method == 'POST':
        # Physically delete the file from storage if desired, 
        # but calling document.delete() usually handles it if configured,
        # or we just delete the db record for now.
        document.file.delete(save=False) # delete actual file
        document.delete()                # delete db record
        
        messages.success(request, "Document deleted successfully.")
        
    return redirect('patients:profile', pk=patient_pk)
