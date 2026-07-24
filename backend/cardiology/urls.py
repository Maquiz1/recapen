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

    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_create, name='category_create'),
    path('categories/edit/<int:pk>/', views.category_edit, name='category_edit'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),
    path('categories/activate/<int:pk>/', views.category_activate, name='category_activate'),
    path('categories/deactivate/<int:pk>/', views.category_deactivate, name='category_deactivate'),
    
    path('types/', views.type_list, name='type_list'),
    path('types/add/', views.type_create, name='type_create'),
    path('types/edit/<int:pk>/', views.type_edit, name='type_edit'),
    path('types/delete/<int:pk>/', views.type_delete, name='type_delete'),
    path('types/activate/<int:pk>/', views.type_activate, name='type_activate'),
    path('types/deactivate/<int:pk>/', views.type_deactivate, name='type_deactivate'),

    path('patients/', views.patient_results_list, name='results_list'),
    path('patients/results/', views.patients_with_results, name='patients_results'),
    path('patients/<int:pk>/', views.patient_results_detail, name='patient_detail'),
    path('orders/pending/', views.pending_orders, name='pending_orders'),
    path('orders/<int:pk>/fulfill/', views.fulfill_order, name='fulfill_order'),
]
