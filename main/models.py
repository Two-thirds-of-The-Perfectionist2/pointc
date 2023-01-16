from django.db import models

from django.contrib.auth import get_user_model


User = get_user_model()



class Products(models.Model):
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    descriptions = models.TextField()

    
class OrganizationCard(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    adress = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=14)
    products = models.ForeignKey(Products, related_name='products')

