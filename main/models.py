from django.db import models

from django.contrib.auth import get_user_model


User = get_user_model()



class Product(models.Model):
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()


class Organization(models.Model):
    user = models.ForeignKey(User, related_name='users', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    adress = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=14)
    product = models.ForeignKey(Product, related_name='products', on_delete=models.CASCADE)

