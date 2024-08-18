from django.db import models
from django.contrib.auth.models import User




from django.db import models

class Inventory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    sku = models.CharField(default= "N/A", max_length=255,)
    price_paid = models.DecimalField(default= 0, max_digits=10, decimal_places=2)
    price_sold = models.DecimalField(default = 0 ,max_digits=10, decimal_places=2, null=True, blank=True)
    size = models.DecimalField(max_digits=4, decimal_places=1)
    condition = models.CharField(max_length=50, choices=[('New', 'New'), ('Used', 'Used'), ('Lightly Used', 'Lightly Used')])
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='inventory_images/', null=True, blank=True, default='default_image.jpg')

    def __str__(self):
        return self.name

