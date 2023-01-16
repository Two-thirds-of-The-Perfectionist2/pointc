from rest_framework.serializers import ModelSerializer

from .models import OrganizationCard, Products

class OrganizationCardSerializer(ModelSerializer):
    class Meta:
        model = OrganizationCard
        fields = '__all__'

class ProductsSerializer(ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'