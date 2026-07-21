from django.urls import path
from . import views

app_name = 'encounters'

urlpatterns = [
    path('<int:patient_id>/log-followup/', views.log_followup, name='log_followup'),
    path('<int:encounter_id>/', views.encounter_detail, name='encounter_detail'),
]
