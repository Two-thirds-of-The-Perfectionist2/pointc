from django_filters.rest_framework import FilterSet
import django_filters

from .models import Organization

class OrganizationFilter(FilterSet):
    class Meta:
        model = Organization
        fields = ['category']