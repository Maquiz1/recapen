from django.urls import path
from . import views

app_name = 'study_config'

urlpatterns = [
    path('', views.config_dashboard, name='dashboard'),
    path('forms/', views.manage_forms, name='manage_forms'),
    path('rules/', views.manage_rules, name='manage_rules'),
]
