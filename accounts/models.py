from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Business(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
