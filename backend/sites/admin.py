from django.contrib import admin
from .models import Site

@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'zone', 'region', 'district', 'is_active')
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'country', 'zone', 'region')
