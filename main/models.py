from django.db import models

from django.contrib.auth import get_user_model


User = get_user_model()


class Organization(models.Model):
    user = models.ForeignKey(User, related_name='users', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=14)
    category = models.CharField(max_length=20, choices=[('Еда', 'Food'), ('Товары', 'Merchandise'), ('Другое', 'Other')])
    tag = models.CharField(max_length=30)
    body = models.TextField()
    cover = models.ImageField(upload_to='organizations')


    @property
    def average_rating(self):
        ratings = self.organization_ratings.all() 
        values = [i.value for i in ratings]

        if values:
            return sum(values) / len(values)

        return 0
    

class Product(models.Model):
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    cover = models.ImageField(upload_to='products')
    organization = models.ForeignKey(Organization, related_name='organizations', on_delete=models.CASCADE)



