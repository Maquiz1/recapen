from django.urls import path
from . import views

app_name = 'departments'

urlpatterns = [
    path('', views.department_list, name='list'),
    path('add/', views.department_create, name='create'),
    path('edit/<int:pk>/', views.department_edit, name='edit'),
    path('deactivate/<int:pk>/', views.department_deactivate, name='deactivate'),
]
