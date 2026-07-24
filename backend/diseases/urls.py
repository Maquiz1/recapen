from django.urls import path
from . import views

app_name = 'diseases'

urlpatterns = [
    path('lists/', views.disease_list, name='disease_list'),
    path('create/', views.disease_create, name='disease_create'),
    path('<int:pk>/edit/', views.disease_update, name='disease_update'),
    path('<int:pk>/deactivate/', views.disease_deactivate, name='disease_deactivate'),
    path('<int:pk>/delete/', views.disease_delete, name='disease_delete'),
]
