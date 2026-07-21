from django.urls import path
from . import views

app_name = 'radiology'

urlpatterns = [
    path('', views.test_list, name='list'),
    path('add/', views.test_create, name='create'),
    path('edit/<int:pk>/', views.test_edit, name='edit'),
    path('edit/', views.test_edit_redirect, name='edit_no_pk'),
    path('results/', views.patient_results_list, name='results_list'),
    path('patients-results/', views.patients_with_results, name='patients_results'),
    path('patients-results/<int:pk>/', views.patient_results_detail, name='patient_results_detail'),
]
