from django.db import models

class Inventory(models.Model):
    CATEGORY_CHOICES = [
        ('Sneakers', 'Sneakers'),
        ('Streetwear', 'Streetwear'),
    ]

    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    sku = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    condition = models.CharField(max_length=50, choices=[('New', 'New'), ('Used', 'Used'), ('Lightly Used', 'Lightly Used')])
    size = models.CharField(max_length=10, default="N/A", null=True, blank=True)
    apparel_size = models.CharField(max_length=10, default="N/A", null=True, blank=True)
    price_paid = models.DecimalField(max_digits=10, decimal_places=2)
    price_sold = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
