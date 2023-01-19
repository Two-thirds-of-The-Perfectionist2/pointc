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


class Cart(models.Model):
    delivery = models.ForeignKey(Delivery, related_name='carts', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='carts', on_delete=models.CASCADE)