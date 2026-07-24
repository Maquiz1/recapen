from django.contrib import admin
from .models import LaboratoryCategory, LaboratoryType, LaboratoryTest, PatientTestResult

@admin.register(LaboratoryCategory)
class LaboratoryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    search_fields = ('name',)

@admin.register(LaboratoryType)
class LaboratoryTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    search_fields = ('name', 'category__name')
    list_filter = ('is_active',)

@admin.register(LaboratoryTest)
class LaboratoryTestAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'laboratory_category', 'laboratory_type', 'cost', 'is_active')
    list_filter = ('laboratory_category', 'laboratory_type', 'is_active')
    search_fields = ('name', 'code')
@admin.register(PatientTestResult)
class PatientTestResultAdmin(admin.ModelAdmin):
    list_display = ('patient', 'test', 'result_value', 'performed_date', 'created_at')
    list_filter = ('performed_date', 'test__laboratory_category')
    search_fields = ('patient__first_name', 'patient__last_name', 'test__name')
