from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('dashboard/', views.appointment_dashboard, name='dashboard'),
    path('list/', views.appointment_list, name='list'),
    path('book/', views.book_appointment, name='book'),
    path('success/', views.appointment_success, name='success'),
    path('<int:pk>/edit/', views.edit_appointment, name='edit'),
    path('<int:pk>/check-in/', views.check_in, name='check_in'),
]
