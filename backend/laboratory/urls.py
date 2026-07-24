from django.urls import path
from . import views

app_name = 'laboratory'

urlpatterns = [
    path('', views.test_list, name='list'),
    path('add/', views.test_create, name='create'),
    path('edit/<int:pk>/', views.test_edit, name='edit'),
    path('edit/', views.test_edit_redirect, name='edit_no_pk'),
    path('activate/<int:pk>/', views.test_activate, name='activate'),
    path('deactivate/<int:pk>/', views.test_deactivate, name='deactivate'),
    path('delete/<int:pk>/', views.test_delete, name='delete'),
    path('patients/', views.patient_results_list, name='results_list'),
    path('patients/results/', views.patients_with_results, name='patients_results'),
    path('patients/<int:pk>/', views.patient_results_detail, name='patient_detail'),
    path('orders/dashboard/', views.lab_dashboard, name='lab_dashboard'),
    path('orders/<int:patient_id>/fulfill/', views.fulfill_lab_order, name='fulfill_order'),
    path('patients/<int:patient_id>/edit_results/<str:date_type>/<str:date_string>/', views.edit_lab_results, name='edit_lab_results'),
]
