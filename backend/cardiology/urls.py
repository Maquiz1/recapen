from django.urls import path
from . import views

app_name = 'cardiology'

urlpatterns = [
    path('', views.test_list, name='list'),
    path('add/', views.test_create, name='create'),
    path('edit/<int:pk>/', views.test_edit, name='edit'),
    path('delete/<int:pk>/', views.test_delete, name='delete'),
    path('activate/<int:pk>/', views.test_activate, name='activate'),
    path('deactivate/<int:pk>/', views.test_deactivate, name='deactivate'),

    path('groups/', views.group_list, name='group_list'),
    path('groups/add/', views.group_create, name='group_create'),
    path('groups/edit/<int:pk>/', views.group_edit, name='group_edit'),
    path('groups/delete/<int:pk>/', views.group_delete, name='group_delete'),
    path('groups/activate/<int:pk>/', views.group_activate, name='group_activate'),
    path('groups/deactivate/<int:pk>/', views.group_deactivate, name='group_deactivate'),
    
    path('groups/', views.group_list, name='group_list'),
    path('groups/add/', views.group_create, name='group_create'),
    path('groups/edit/<int:pk>/', views.group_edit, name='group_edit'),
    path('groups/delete/<int:pk>/', views.group_delete, name='group_delete'),
    path('groups/activate/<int:pk>/', views.group_activate, name='group_activate'),
    path('groups/deactivate/<int:pk>/', views.group_deactivate, name='group_deactivate'),

    path('patients/', views.patient_results_list, name='results_list'),
    path('patients/results/', views.patients_with_results, name='patients_results'),
    path('patients/<int:pk>/', views.patient_results_detail, name='patient_detail'),
    path('orders/pending/', views.pending_orders, name='pending_orders'),
    path('orders/<int:pk>/fulfill/', views.fulfill_order, name='fulfill_order'),
]
