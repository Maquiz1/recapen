from django.urls import path
from . import views

app_name = 'laboratory'

urlpatterns = [
    path('', views.test_list, name='list'),
    path('add/', views.test_create, name='create'),
    path('edit/<int:pk>/', views.test_edit, name='edit'),
    path('edit/', views.test_edit_redirect, name='edit_no_pk'),
]
