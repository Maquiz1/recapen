from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('<int:patient_id>/upload/', views.upload_document, name='upload'),
    path('<int:pk>/delete/', views.delete_document, name='delete'),
]
