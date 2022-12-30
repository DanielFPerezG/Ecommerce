from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Product(models.Model):
    name = models.CharField(max_length=150,null=True)
    bio = models.CharField(max_length=1000,null=True)
    image = models.ImageField(null=True)
    price = models.PositiveIntegerField(null=True)
    stock = models.PositiveIntegerField(null=True)
    topic = models.CharField(max_length=150, null=True)
    cost = models.PositiveIntegerField(null=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-updated','-created']
    