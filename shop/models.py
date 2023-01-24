from decimal import Decimal
from django.contrib.gis.db import models
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.contrib.auth import get_user_model

from main.models import Product



User = get_user_model()


class Delivery(models.Model):
    address = models.CharField(max_length=32)
    location = models.PointField(null=True)
    phone = models.CharField(max_length=24)
    body = models.TextField(null=True)
    customer = models.ForeignKey(User, related_name='customers', on_delete=models.CASCADE)
    deliveryman = models.ForeignKey(User, related_name='deliveries', on_delete=models.CASCADE, null=True)
    activation_code = models.CharField(max_length=8, null=True)


    def create_activation_code(self):
        from django.utils.crypto import get_random_string

        code = get_random_string(length=8, allowed_chars='qwertyuiopasdfghjklzxcvbnmQWERTYUIOASDFGHJKLZXCVBNM234567890')
        self.activation_code = code
        self.save()


    @property
    def price(self):
        carts = self.carts.all()
        products = sum([i.product.price for i in carts])
        
        query = Delivery.objects.annotate(distance=Distance('location', self.carts.first().product.organization.location)).filter(id=self.id).first()

        print(query.distance)
        
        if query.distance < D(m=3000):
            delivery = products * Decimal(0.05)
        elif query.distance < D(m=12000):
            delivery = products * Decimal(0.15)
        else:
            raise Exception('Не удалось подтвердить Ваш заказ: расстояние превышает допустимое.')
        
        return {'products': products, 'delivery': delivery}


class Cart(models.Model):
    delivery = models.ForeignKey(Delivery, related_name='carts', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='carts', on_delete=models.CASCADE)
