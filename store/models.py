from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    VENDOR = 'V'
    BUYER = 'B'
    ROLE_CHOICES = [(VENDOR, 'Vendor'), (BUYER, 'Buyer')]
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, default=BUYER)

class Store(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
