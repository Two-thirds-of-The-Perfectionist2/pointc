from rest_framework.serializers import ModelSerializer

from .models import OrganizationCard, Products

class OrganizationCardSerializer(ModelSerializer):
    class Meta:
        model = OrganizationCard
        exclude = ('user',)

    def validate(self, attrs):
        attrs =  super().validate(attrs)
        request = self.context.get('request')
        attrs['user'] = request.user
        return attrs

class ProductsSerializer(ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'