from django.urls import path
from . import views

app_name = 'clinical'

urlpatterns = [
    path('encounter/<int:encounter_id>/form/<str:form_code>/', views.fill_form, name='fill_form'),
]
