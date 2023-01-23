from django.db import models
from django.contrib.auth import get_user_model

from main.models import Product



User = get_user_model()


class Delivery(models.Model):
    address = models.CharField(max_length=32)
    phone = models.CharField(max_length=16)
    body = models.TextField()
    customer = models.ForeignKey(User, related_name='customers', on_delete=models.CASCADE)
    deliveryman = models.ForeignKey(User, related_name='deliveries', on_delete=models.CASCADE, null=True)
    activation_code = models.CharField(max_length=8, null=True)


    def create_activation_code(self):
        from django.utils.crypto import get_random_string

        code = get_random_string(length=8, allowed_chars='qwertyuiopasdfghjklzxcvbnmQWERTYUIOASDFGHJKLZXCVBNM234567890')
        self.activation_code = code
        self.save()


    @property
    def amount(self):
        carts =  self.carts.all()
        prices = sum([i.product.price for i in carts])
        DELIVERY_AMOUNT = 100
        total = prices + DELIVERY_AMOUNT

        return total


class Cart(models.Model):
    delivery = models.ForeignKey(Delivery, related_name='carts', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='carts', on_delete=models.CASCADE)
