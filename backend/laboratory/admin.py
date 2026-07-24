from django.contrib import admin
from .models import PatientTestResult

@admin.register(PatientTestResult)
class PatientTestResultAdmin(admin.ModelAdmin):
    list_display = ('patient', 'test', 'result_value', 'performed_date', 'created_at')
    list_filter = ('performed_date',)
    search_fields = ('patient__first_name', 'patient__last_name', 'test__test_name')
