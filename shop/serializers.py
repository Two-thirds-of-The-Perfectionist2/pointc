from rest_framework import serializers

from .models import Delivery, Cart


class DeliverySerializer(serializers.ModelSerializer):

    class Meta:
        model = Delivery
        exclude = ('customer',)
    

    def validate(self, attrs):
        attrs = super().validate(attrs)
        request = self.context.get('request')
        attrs['customer'] = request.user

        return attrs
    

    def to_representation(self, instance):
        # print(instance.carts.delivery)
        rep = super().to_representation(instance)
        rep['cart'] = CartSerializer(instance.carts.all(), many=True).data
        rep['total'] = instance.amount

        return rep


class DeliveryManSerializer(serializers.ModelSerializer):

    class Meta:
        model = Delivery
        exclude = ('deliveryman',)
    

    def validate(self, attrs):
        attrs = super().validate(attrs)
        request = self.context.get('request')
        attrs['deliveryman'] = request.user

        return attrs
    


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        exclude = ('delivery',)
    

    def validate(self, attrs):
        attrs = super().validate(attrs)
        request = self.context.get('request')
        attrs['delivery'] = request.data.get('delivery')

        return attrs
