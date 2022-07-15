from django.db import models


class User(models.Model):
    username = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)
