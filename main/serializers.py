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

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user'] = instance.user.email
        rep['ratings'] = instance.average_rating
        rep['likes'] = instance.likes.count()
        rep['products'] = ProductSerializer(instance.products.all(), many=True).data

        return rep


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    