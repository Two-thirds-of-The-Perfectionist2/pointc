from django.db import models

from django.contrib.auth import get_user_model


User = get_user_model()


class Organization(models.Model):
    title = models.CharField(max_length=24)
    address = models.CharField(max_length=32)
    phone_number = models.CharField(max_length=24)
    category = models.CharField(max_length=24, choices=[('Еда', 'Food'), ('Товары', 'Merchandise'), ('Другое', 'Other')])
    tag = models.CharField(max_length=24, blank=True)
    body = models.TextField(blank=True)
    cover = models.ImageField(upload_to='organizations', default='default/organization.jpg')
    user = models.ForeignKey(User, related_name='organizations', on_delete=models.CASCADE)
    

    @property
    def average_rating(self):
        ratings = self.organization_ratings.all() 
        values = [i.value for i in ratings]

        if values:
            return sum(values) / len(values)

        return 0
    

class Product(models.Model):
    title = models.CharField(max_length=24)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    cover = models.ImageField(upload_to='products', default='default/product.jpg')
    organization = models.ForeignKey(Organization, related_name='products', on_delete=models.CASCADE)
