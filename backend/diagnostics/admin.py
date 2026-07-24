from django.contrib import admin
from .models import DiagnosticGroup, DiagnosticCategory, DiagnosticTest

@admin.register(DiagnosticGroup)
class DiagnosticGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'is_active', 'created_at')
    search_fields = ('name', 'department__name')

@admin.register(DiagnosticCategory)
class DiagnosticCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'is_active', 'created_at')
    search_fields = ('name', 'group__name')
    list_filter = ('is_active',)

@admin.register(DiagnosticTest)
class DiagnosticTestAdmin(admin.ModelAdmin):
    list_display = ('test_name', 'code', 'department', 'diagnostic_group', 'diagnostic_category', 'cost', 'is_active')
    list_filter = ('department', 'diagnostic_group', 'diagnostic_category', 'is_active')
    search_fields = ('test_name', 'code')
