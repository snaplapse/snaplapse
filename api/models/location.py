from django.db import models
from . import Category


class Location(models.Model):
    name = models.CharField(max_length=64)
    longitude = models.FloatField()
    latitude = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category)
