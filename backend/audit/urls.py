from django.urls import path
from . import views

app_name = 'audit'

urlpatterns = [
    path('', views.audit_dashboard, name='dashboard'),
    path('patient/<int:pk>/', views.patient_history, name='patient_history'),
]
