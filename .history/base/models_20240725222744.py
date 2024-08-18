from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


from django.db import models
import time

class Inventory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length= 50,null=True, blank=True)
    sku = models.CharField(default= "N/A", max_length=255,)
    price_paid = models.DecimalField(default= 0, max_digits=10, decimal_places=2)
    price_sold = models.DecimalField(default = 0 ,max_digits=10, decimal_places=2, null=True, blank=True)
    size = models.CharField(default= "N/A", max_length=10, null=True, blank=True)
    condition = models.CharField(default= "New",max_length=50, choices=[('New', 'New'), ('Used', 'Used'), ('Lightly Used', 'Lightly Used')])
    quantity = models.PositiveIntegerField()
    category = models.CharField(default= "Sneakers", max_length=50, choices=[('Sneakers', 'Sneakers'),('Streetwear', 'Streetwear')])
    imageUrl = models.URLField(max_length=200, null=True, blank=True, default='https://example.com/default_image.jpg')
    apparel_size = models.CharField(max_length=255, default="N/A")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)  # This will automatically set the default value to the current date and time




 # This will automatically set the default value to the current date and time

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-updated', '-created']