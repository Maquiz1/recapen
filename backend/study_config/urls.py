from django.urls import path
from . import views

app_name = 'study_config'

urlpatterns = [
    path('', views.config_dashboard, name='dashboard'),
    path('forms/', views.manage_forms, name='manage_forms'),
    path('rules/', views.manage_rules, name='manage_rules'),
    path('rules/<int:rule_id>/remove-form/<int:form_id>/', views.remove_form_from_rule, name='remove_form_from_rule'),
    path('rules/<int:rule_id>/delete/', views.delete_rule, name='delete_rule'),
]
