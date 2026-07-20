from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin, name='admin'),
    path('medical/', views.medical, name='medical'),
    path('clinic/', views.clinic, name='clinic'),
]
