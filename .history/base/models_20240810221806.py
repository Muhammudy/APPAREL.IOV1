from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.core.exceptions import ValidationError

class Inventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    name = models.CharField(max_length=255)
    description = models.TextField(maxlength=50, null=True, blank=True)
    sku = models.CharField(default="N/A", maxlength=255)
    price_paid = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    price_sold = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    profit = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    size = models.CharField(default="N/A", max_length=10, null=True, blank=True)
    condition = models.CharField(max_length=50, choices=[('New', 'New'), ('Used', 'Used'), ('Lightly Used', 'Lightly Used')])
    quantity = models.PositiveIntegerField(default=1)
    sold_quantity = models.PositiveIntegerField(default=0, editable=False)  # Track sold items separately
    category = models.CharField(blank=True, default="Sneakers", max_length=50, choices=[('Sneakers', 'Sneakers'), ('Streetwear', 'Streetwear')])
    imageUrl = models.URLField(maxlength=200, null=True, blank=True, default='https://example.com/default_image.jpg')
    status = models.CharField(default="Available", max_length=50, choices=[('Sold', 'Sold'), ('Available', 'Available')])
    apparel_size = models.CharField(blank=True, max_length=255, default="N/A")
    image = models.ImageField(default='images/default_image.jpg', upload_to='images/', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def clean(self):
        # Validate that price_sold is set and greater than zero when marking as Sold
        if self.status == 'Sold':
            if self.price_sold is None or self.price_sold <= Decimal(0):
                raise ValidationError("Price sold must be set and greater than zero when marking an item as Sold.")

    def save(self, *args, **kwargs):
        if self.pk:
            original = Inventory.objects.get(pk=self.pk)
            original_status = original.status
            original_quantity = original.quantity
            original_sold_quantity = original.sold_quantity
        else:
            original_status = None
            original_quantity = 0
            original_sold_quantity = 0

        super(Inventory, self).save(*args, **kwargs)
        print("Debug: Inventory item saved successfully.")

        # Handle transitions between Available and Sold statuses
        if original_status != self.status:
            if self.status == 'Sold':
                # Increase sold quantity and reduce available quantity
                self.sold_quantity += self.quantity
                profile = self.get_profile()
                profile.sold_count += self.quantity
                profile.save()
                print("Debug: Marked as Sold. Sold quantity incremented.")
            elif original_status == 'Sold' and self.status == 'Available':
                # If transitioning back to Available, restore the quantity
                self.quantity += original_sold_quantity
                self.sold_quantity = 0
                profile = self.get_profile()
                profile.sold_count -= original_sold_quantity
                profile.save()
                print("Debug: Status reverted to Available. Quantity restored.")

        # Update the profit count
        self.increment_profit_count()

    def increment_profit_count(self):
        profile = self.get_profile()
        if self.profit is not None:
            profile.profit_count += self.profit
            print(f"Debug: Incremented profit by {self.profit}. New profit count: {profile.profit_count}")
        profile.save()

    def get_profile(self):
        # Use the user associated with this inventory item to find the related profile
        return Profile.objects.get(user=self.user)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-updated', '-created']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    secondary_email = models.EmailField(maxlength=254, blank=True)
    phone_number = models.CharField(maxlength=15, blank=True)
    profile_pic = models.ImageField(default='profile_pic/default_image.jpg', upload_to='profile_pic/', null=True, blank=True)
    instagram = models.URLField(maxlength=200, blank=True)
    inventory_link = models.URLField(maxlength=200, blank=True)
    profit_goal = models.DecimalField(max_digits=10, decimal_places=2, default=1000, validators=[MinValueValidator(0)])
    sales_goal = models.PositiveIntegerField(default=100)
    inventory_goal = models.PositiveIntegerField(default=100)
    sold_count = models.IntegerField(default=0, editable=False)  # total sales count
    inventory_count = models.IntegerField(default=0, editable=False)  # total inventory
    profit_count = models.DecimalField(default=0, max_digits=100, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
