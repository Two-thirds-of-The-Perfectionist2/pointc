from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(OrganizationComment)
admin.site.register(OrganizationRating)
admin.site.register(UserRating)
admin.site.register(ProductFavorite)
admin.site.register(OrganizationLike)