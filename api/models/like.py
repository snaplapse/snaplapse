from django.db import models

from .photo import Photo
from .user import User


class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, related_name='likes', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'photo')
