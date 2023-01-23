from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from .models import Cart, Delivery


class CartInline(admin.TabularInline):
    model = Cart


@admin.register(Delivery)
class DeliveryAdmin(OSMGeoAdmin):
    list_display = ('address', 'phone', 'location')


admin.site.register(Cart)     
