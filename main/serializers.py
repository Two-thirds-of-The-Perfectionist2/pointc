from decouple import config
from rest_framework.serializers import ModelSerializer

from .models import Organization, Product
from review.models import Subscription


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
        rep['subscribers'] = instance.subscriptions.count()
        rep['cover'] = f"http://{config('CURRENT_HOST')}/media/{instance.cover}"

        return rep


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['organization'] = instance.organization.title
        rep['cover'] = f"http://{config('CURRENT_HOST')}/media/{instance.cover}"

        return rep
    
    

class SubscriptionSerializer(ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'
    

    def validate(self, attrs):
        attrs =  super().validate(attrs)
        request = self.context.get('request')
        attrs['user'] = request.user
        
        return attrs