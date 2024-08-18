from django.db import models

class Inventory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default= "N/A")
    sku = models.CharField(max_length=255, unique=True)
    price_paid = models.DecimalField(max_digits=10, decimal_places=2)
    price_sold = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    size = models.DecimalField(max_digits=4, decimal_places=1)
    condition = models.CharField(max_length=50, choices=[('New', 'New'), ('Used', 'Used'), ('Lightly Used', 'Lightly Used')])
    quantity = models.PositiveIntegerField()
    category = models.CharField(max_length=50, choices=[('Sneakers', 'Sneakers'), ('Streetwear', 'Streetwear')])
    image = models.ImageField(upload_to='inventory_images/', null=True, blank=True)

    def __str__(self):
        return self.name
