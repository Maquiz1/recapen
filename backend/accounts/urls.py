from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('doctors/grid/', views.doctor_list_grid, name='grid'),
    path('doctors/cards/', views.doctor_list_cards, name='cards'),
    path('doctors/add/', views.doctor_create, name='create'),
    path('doctors/edit/<int:pk>/', views.doctor_edit, name='edit'),
    path('doctors/edit/', views.doctor_edit_redirect, name='edit_no_pk'),
    path('doctors/profile/<int:pk>/', views.doctor_profile, name='profile'),
    path('doctors/profile/', views.doctor_profile_redirect, name='profile_no_pk'),
    path('doctors/dashboard/<int:pk>/', views.doctor_dashboard, name='dashboard'),
    path('doctors/dashboard/', views.doctor_dashboard_redirect, name='dashboard_no_pk'),
]
