from django.urls import path
from . import views

app_name = 'medications'

urlpatterns = [
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/<int:pk>/update/', views.update_inventory, name='update_inventory'),
]
