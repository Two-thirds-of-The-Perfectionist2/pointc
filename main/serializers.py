from rest_framework.serializers import ModelSerializer

from .models import Organization, Product

class OrganizationSerializer(ModelSerializer):
    class Meta:
        model = Organization
        exclude = ('user',)

    def validate(self, attrs):
        attrs =  super().validate(attrs)
        request = self.context.get('request')
        attrs['user'] = request.user
        return attrs

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'