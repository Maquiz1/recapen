from django.urls import path
from . import views

app_name = 'pharmacy'

urlpatterns = [
    path('pending/', views.pending_prescriptions, name='pending_prescriptions'),
    path('<int:pk>/fulfill/', views.fulfill_prescription, name='fulfill_prescription'),
]
