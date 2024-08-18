from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.core.exceptions import ValidationError
class Inventory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=50, null=True, blank=True)
    sku = models.CharField(default="N/A", max_length=255)
    price_paid = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    price_sold = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    profit = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    size = models.CharField(default="N/A", max_length=10, null=True, blank=True)
    condition = models.CharField(max_length=50, choices=[('New', 'New'), ('Used', 'Used'), ('Lightly Used', 'Lightly Used')])
    quantity = models.PositiveIntegerField(default=1)
    category = models.CharField(blank=True, default="Sneakers", max_length=50, choices=[('Sneakers', 'Sneakers'), ('Streetwear', 'Streetwear')])
    imageUrl = models.URLField(max_length=200, null=True, blank=True, default='https://example.com/default_image.jpg')
    status = models.CharField(default="Available", max_length=50, choices=[('Sold', 'Sold'), ('Available', 'Available')])
    apparel_size = models.CharField(blank=True, max_length=255, default="N/A")
    image = models.ImageField(default='images/default_image.jpg', upload_to='images/', null=True, blank=True)
    sold_count = models.IntegerField(default=0, editable=False)
    inventory_count = models.IntegerField(default=0, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def clean(self):
        # Validate that price_sold is set and greater than zero when marking as Sold
        if self.status == 'Sold':
            if self.price_sold is None or self.price_sold <= Decimal(0):
                raise ValidationError("Price sold must be set and greater than zero when marking an item as Sold.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensure that validations are checked before saving
        if self.status == 'Sold' and not self.pk:  # Only increment on first save as "Sold"
            self.increment_sold_count()
        if self.price_sold is not None:
            self.profit = self.price_sold - self.price_paid
        else:
            self.profit = Decimal(0)
        super(Inventory, self).save(*args, **kwargs)

    def increment_sold_count(self):
        self.sold_count += 1

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-updated', '-created']




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    secondary_email = models.EmailField(max_length=254, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    profile_pic = models.ImageField(default='profile_pic/default_image.jpg', upload_to='profile_pic/', null=True, blank=True)
    instagram = models.URLField(max_length=200, blank=True)
    inventory_link = models.URLField(max_length=200, blank = True)
    profit_goal = models.DecimalField(max_digits=10, decimal_places=2, default=1000, validators=[MinValueValidator(0)])
    sales_goal = models.PositiveIntegerField(default=100)
    inventory_goal = models.PositiveIntegerField(default=100)

    def __str__(self):
        return f'{self.user.username} Profile'
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()   