from django.db import models

from book.models import User
from main.models import OrganizationCard


class OrganizationComment(models.Model):
    user_id = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    organization_id = models.ForeignKey(OrganizationCard, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return f'{self.user_id} -> {self.organization_id}'