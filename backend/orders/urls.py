from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('prescribe/<int:encounter_id>/', views.prescribe_medication, name='prescribe'),
]
