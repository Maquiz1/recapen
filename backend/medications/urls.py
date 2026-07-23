from django.urls import path
from . import views

app_name = 'medications'

urlpatterns = [
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/add/', views.create_medication, name='create'),
    path('inventory/<int:pk>/edit/', views.edit_medication, name='edit'),
]
