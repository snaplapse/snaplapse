from django.db import models

from .category import Category
from .location import Location


class Tag(models.Model):
    location = models.ForeignKey(Location, related_name='tags', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='tags', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
