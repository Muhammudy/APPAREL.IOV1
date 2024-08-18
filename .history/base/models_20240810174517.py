from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator
from decimal import Decimal

class Inventory(models.Model):
    # Your existing fields...
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=50, null=True, blank=True)
    sku = models.CharField(default="N/A", max_length=255)
    price_paid = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    price_sold = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    profit = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    size = models.CharField(default="N/A", max_length=10, null=True, blank=True)
    condition = models.CharField(max_length=50, choices=[('New', 'New'), ('Used', 'Used'), ('Lightly Used', 'Lightly Used')])
    quantity = models.PositiveIntegerField(default=1)
    category = models.CharField(blank= True, default="Sneakers", max_length=50, choices=[('Sneakers', 'Sneakers'), ('Streetwear', 'Streetwear')])
    imageUrl = models.URLField(max_length=200, null=True, blank=True, default='https://example.com/default_image.jpg')
    status = models.CharField(default= "Available", max_length=50, choices=[('Sold', 'Sold'), ('Available', 'Available')])
    apparel_size = models.CharField(blank= True, max_length=255, default="N/A")
    image = models.ImageField(default='images/default_image.jpg', upload_to='images/', null=True, blank=True)
    sold_count = models.IntegerField(default=0, editable=False)
    inventory_count = models.IntegerField(default= 0, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.pk:
            original_status = Inventory.objects.get(pk=self.pk).status
            if original_status != 'Sold' and self.status == 'Sold':
                self.increment_sold_count()
                self.increment_total_profit()
        elif self.status == 'Sold':
            self.increment_sold_count()
            self.increment_total_profit()

        # Calculate profit or set to None
        if self.price_sold and self.price_sold > Decimal(0):
            self.profit = Decimal(self.price_sold) - Decimal(self.price_paid)
        else:
            self.profit = None  # Set profit to None if sale price is 0.00

        super(Inventory, self).save(*args, **kwargs)

    def increment_sold_count(self):
        self.sold_count += 1
        profile = self.get_profile()
        profile.total_sales += 1
        profile.save()

    def increment_total_profit(self):
        profile = self.get_profile()
        profile.total_profit += self.profit
        profile.save()

    def get_profile(self):
        return Profile.objects.get(user=self.user)  # Assuming each Inventory is tied to a user

    class Meta:
        ordering = ['-updated', '-created']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    secondary_email = models.EmailField(max_length=254, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    profile_pic = models.ImageField(default='profile_pic/default_image.jpg', upload_to='profile_pic/', null=True, blank=True)
    instagram = models.URLField(max_length=200, blank=True)
    inventory_link = models.URLField(max_length=200, blank=True)
    profit_goal = models.DecimalField(max_digits=10, decimal_places=2, default=1000, validators=[MinValueValidator(0)])
    sales_goal = models.PositiveIntegerField(default=100)
    inventory_goal = models.PositiveIntegerField(default=100)
    total_sales = models.PositiveIntegerField(default=0)
    total_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_inventory = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} Profile'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
