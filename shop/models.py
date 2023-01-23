from django.contrib.gis.db import models
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

    @property
    def price(self):
        carts =  self.carts.all()
        prices = sum([i.product.price for i in carts])
        DELIVERY_AMOUNT = 100
        total = prices + DELIVERY_AMOUNT

        return total


class Cart(models.Model):
    delivery = models.ForeignKey(Delivery, related_name='carts', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='carts', on_delete=models.CASCADE)
