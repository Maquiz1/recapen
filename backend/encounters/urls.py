from django.urls import path
from . import views

app_name = 'encounters'

urlpatterns = [
    path('missing-medications/', views.missing_meds_list, name='missing_meds_list'),
    path('<int:patient_id>/log-followup/', views.log_followup, name='log_followup'),
    path('<int:patient_id>/log-scheduled-visit/', views.log_scheduled_visit, name='log_scheduled_visit'),
    path('<int:encounter_id>/', views.encounter_detail, name='encounter_detail'),
    path('<int:encounter_id>/update-nature/', views.update_visit_nature, name='update_visit_nature'),
    path('<int:encounter_id>/prescriptions/add/', views.manage_prescription, name='add_prescription'),
    path('<int:encounter_id>/prescriptions/<int:prescription_id>/edit/', views.manage_prescription, name='edit_prescription'),
]
