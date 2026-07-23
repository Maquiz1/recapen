from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import PatientDocument
from .forms import DocumentUploadForm
from patients.models import Patient

def upload_document(request, encounter_id):
    from encounters.models import Encounter
    encounter = get_object_or_404(Encounter, pk=encounter_id)
    patient = encounter.patient
    
    if request.method == 'POST':
        document_types = request.POST.getlist('document_type')
        descriptions = request.POST.getlist('description')
        files = request.FILES.getlist('file')
        
        added_count = 0
        
        for i in range(len(files)):
            doc_type = document_types[i] if i < len(document_types) else 'other'
            desc = descriptions[i] if i < len(descriptions) else ''
            file_obj = files[i]
            
            if file_obj:
                PatientDocument.objects.create(
                    patient=patient,
                    encounter=encounter,
                    file=file_obj,
                    document_type=doc_type,
                    description=desc,
                    uploaded_by=request.user if request.user.is_authenticated else None,
                    created_by=request.user if request.user.is_authenticated else None,
                    updated_by=request.user if request.user.is_authenticated else None
                )
                added_count += 1
                
        if added_count > 0:
            messages.success(request, f"Successfully uploaded {added_count} document(s) for {patient}.")
        else:
            messages.error(request, "No documents were uploaded.")
            
        return redirect('encounters:encounter_detail', encounter_id=encounter.pk)
    else:
        form = DocumentUploadForm()
        
    return render(request, 'documents/upload.html', {'form': form, 'patient': patient, 'encounter': encounter})

def delete_document(request, pk):
    document = get_object_or_404(PatientDocument, pk=pk)
    patient_pk = document.patient.pk
    
    encounter_pk = document.encounter.pk if document.encounter else None
    
    if request.method == 'POST':
        # Physically delete the file from storage if desired, 
        # but calling document.delete() usually handles it if configured,
        # or we just delete the db record for now.
        document.file.delete(save=False) # delete actual file
        document.delete()                # delete db record
        
        messages.success(request, "Document deleted successfully.")
        
    if encounter_pk:
        return redirect('encounters:encounter_detail', encounter_id=encounter_pk)
    return redirect('patients:profile', pk=patient_pk)

def replace_document(request, pk):
    document = get_object_or_404(PatientDocument, pk=pk)
    encounter_pk = document.encounter.pk if document.encounter else None
    patient_pk = document.patient.pk
    
    if request.method == 'POST':
        new_file = request.FILES.get('file')
        if new_file:
            # Delete old file
            if document.file:
                document.file.delete(save=False)
            
            # Save new file
            document.file = new_file
            if request.user.is_authenticated:
                document.updated_by = request.user
            document.save()
            
            messages.success(request, f"Document replaced successfully.")
        else:
            messages.error(request, "No file provided for replacement.")
            
    if encounter_pk:
        return redirect('encounters:encounter_detail', encounter_id=encounter_pk)
    return redirect('patients:profile', pk=patient_pk)
