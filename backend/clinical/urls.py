from django.urls import path
from . import views

app_name = 'clinical'

urlpatterns = [
    path('encounter/<int:encounter_id>/form/<str:form_code>/', views.fill_form, name='fill_form'),
    path('prescriptions/', views.prescription_list, name='prescription_list'),
    path('enrollment/<int:enrollment_id>/baselines/', views.baseline_forms, name='baseline_forms'),
]
