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
        request = self.context.get('request')

        if not instance.deliveryman or request.user == instance.deliveryman:
            rep = super().to_representation(instance)
            rep['title organization'] = instance.carts.first().product.organization.title
            rep['title product'] = instance.carts.first().product.title
            rep['organization address'] = instance.carts.first().product.organization.address
            rep['organization phone'] = instance.carts.first().product.organization.phone
            rep['cart'] = CartSerializer(instance.carts.all(), many=True).data
            rep['price'] = instance.price.get('delivery')

            return rep
        
        return f'Заказ {instance.id} недоступен.'


    def create(self, validated_data):
        delivery = Delivery.objects.create(**validated_data)
        delivery.create_activation_code()

        return delivery


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


class HistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Delivery
        exclude = ('customer',)
    

    def validate(self, attrs):
        attrs = super().validate(attrs)
        request = self.context.get('request')
        attrs['customer'] = request.user

        return attrs
    

    def to_representation(self, instance):
        if instance.activation_code:
            return f'Заказ {instance.id} еще не подтвержден.'

        rep = super().to_representation(instance)
        rep['cart'] = CartSerializer(instance.carts.all(), many=True).data
        rep['price'] = instance.price

        return rep
        

    def create(self, validated_data):
        delivery = Delivery.objects.create(**validated_data)
        delivery.create_activation_code()

        return delivery