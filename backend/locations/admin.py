from django.contrib import admin
from .models import Country, Zone, Region, District, Ward

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name', 'country__name')
    list_filter = ('country',)

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'zone')
    search_fields = ('name', 'zone__name')
    list_filter = ('zone',)

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'region')
    search_fields = ('name', 'region__name')
    list_filter = ('region',)

@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ('name', 'district')
    search_fields = ('name', 'district__name')
    list_filter = ('district',)
