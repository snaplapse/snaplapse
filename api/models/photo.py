from django.db import models

from .location import Location
from .user import User


class Photo(models.Model):
    user = models.ForeignKey(User, related_name='photos', on_delete=models.CASCADE)
    location = models.ForeignKey(Location, related_name='photos', on_delete=models.CASCADE)
    description = models.CharField(max_length=256)
    visible = models.BooleanField(default=False)
    bitmap = models.BinaryField()
    created = models.DateTimeField(auto_now_add=True)
