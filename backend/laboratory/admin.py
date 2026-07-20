from django.contrib import admin
from .models import LabTest, PatientTestResult

@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'category', 'is_active', 'created_at')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'code')
    filter_horizontal = ('diseases',)

@admin.register(PatientTestResult)
class PatientTestResultAdmin(admin.ModelAdmin):
    list_display = ('patient', 'test', 'result_value', 'performed_date', 'created_at')
    list_filter = ('performed_date', 'test__category')
    search_fields = ('patient__first_name', 'patient__last_name', 'test__name')
