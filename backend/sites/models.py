from django.db import models
from locations.models import Country, Zone, Region, District, Ward

class Site(models.Model):
    name = models.CharField(max_length=200, unique=True)
    site_code = models.CharField(max_length=10, unique=True, help_text="e.g. KND for Kondoa")
    description = models.TextField(blank=True, null=True)
    
    # Location Hierarchy
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, related_name='sites')
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, null=True, related_name='sites')
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, related_name='sites')
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, related_name='sites')
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True, related_name='sites')
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
