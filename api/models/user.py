from django.db import models


class User(models.Model):
    username = models.CharField(max_length=16, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    secret = models.CharField(max_length=128, null=False, default="snaplapse")