from django.db import models
from django.contrib.auth import get_user_model

from main.models import Organization

User = get_user_model()


class OrganizationComment(models.Model):
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return f'{self.user_id} -> {self.organization_id}'


class OrganizationRating(models.Model):
    value = models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])
    user = models.ForeignKey(User, related_name='organization_ratings', on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, related_name='organization_ratings', on_delete=models.CASCADE)


class UserRating(models.Model):
    value = models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])
    customer = models.ForeignKey(User, related_name='customer_ratings', on_delete=models.CASCADE)
    deliveryman = models.ForeignKey(User, related_name='deliveryman_ratings', on_delete=models.CASCADE)