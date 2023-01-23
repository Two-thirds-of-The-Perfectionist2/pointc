from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from .models import Organization, Product


@admin.register(Organization)
class OrganizationAdmin(OSMGeoAdmin):
    list_display = ('title', 'address', 'location')

admin.site.register(Product)
