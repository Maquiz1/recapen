from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('prescribe/<int:patient_id>/', views.prescribe_medication, name='prescribe'),
]
