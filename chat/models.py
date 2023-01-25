from django.db import models
from datetime import datetime


class Room(models.Model):
    name = models.CharField(max_length=24)


class Message(models.Model):
    value = models.CharField(max_length=256)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=24)
    room = models.CharField(max_length=24)
