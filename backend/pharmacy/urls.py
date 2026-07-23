from django.urls import path
from . import views

app_name = 'pharmacy'

urlpatterns = [
    path('batches/', views.batch_list, name='batch_list'),
    path('dispensations/', views.dispensation_list, name='dispensation_list'),
    path('dispense/<int:prescription_id>/', views.dispense_prescription, name='dispense_prescription'),
    path('low-stock/', views.low_stock_list, name='low_stock_list'),
    path('expiring-soon/', views.expiring_soon_list, name='expiring_soon_list'),
    path('expired/', views.expired_list, name='expired_list'),
]
