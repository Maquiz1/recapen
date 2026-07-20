from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('', views.patient_list, name='list'),
    path('diagnosis/', views.patient_diagnosis_list, name='diagnosis_list'),
    path('register/', views.patient_register, name='register'),
    path('screening/<int:pk>/', views.patient_screening, name='screening'),
    path('investigation/<int:pk>/', views.patient_investigation, name='investigation'),
    path('consultation/<int:pk>/', views.patient_consultation, name='consultation'),
    path('enrollment/<int:pk>/', views.patient_enrollment, name='enrollment'),
    path('profile/<int:pk>/', views.patient_profile, name='profile'),
    path('my-patients/', views.my_patients, name='my_patients'),
    path('edit/<int:pk>/', views.patient_edit, name='edit'),
    path('dashboard/<int:pk>/', views.patient_dashboard, name='dashboard'),
    path('dashboard/', views.patient_dashboard_redirect, name='dashboard_no_pk'),
    path('profile/', views.patient_profile_redirect, name='profile_no_pk'),
    path('edit/', views.patient_edit_redirect, name='edit_no_pk'),
]
