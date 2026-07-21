from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('calendar/', views.daily_calendar, name='calendar'),
    path('book/<int:patient_id>/', views.book_appointment, name='book'),
    path('<int:pk>/check-in/', views.check_in, name='check_in'),
]
