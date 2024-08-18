from django.db import models
from django.contrib.auth.models import User

# Inventory model to represent the inventory items
class Inventory(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    sku = models.CharField(max_length=100, unique=True, null=True, blank=True, default='SKU')  # Add SKU field
    price_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Add Price Paid field
    price_sold = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Add Price Sold field
    size = models.IntegerField(default=0)
    condition = models.CharField(max_length=20, default="New")
    quantity = models.IntegerField(default=1)  # Add Quantity field
    category = models.CharField(max_length=200, default="Sneaker")
    image = models.CharField(max_length=255, default='default_image.jpg')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name
