from django.contrib import admin

from .models import Cart, Delivery


class CartInline(admin.TabularInline):
    model = Cart

class DeliveryAdmin(admin.ModelAdmin):
    inlines = [CartInline]

# admin.site.register(Cart)     
admin.site.register(Delivery,DeliveryAdmin)