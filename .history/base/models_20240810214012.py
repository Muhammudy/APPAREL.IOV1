from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.core.exceptions import ValidationError

class Inventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Assuming user with ID 1 exists

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
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def clean(self):
        # Validate that price_sold is set and greater than zero when marking as Sold
        if self.status == 'Sold':
            if self.price_sold is None or self.price_sold <= Decimal(0):
                raise ValidationError("Price sold must be set and greater than zero when marking an item as Sold.")

    def save(self, *args, **kwargs):
        if self.pk:
            print(f"Debug: Saving inventory item with ID {self.pk}")
            original = Inventory.objects.get(pk=self.pk)
            original_status = original.status
            original_quantity = original.quantity
            original_profit = original.profit or Decimal(0)
        else:
            print("Debug: Creating a new inventory item (ID is None)")
            original_status = None
            original_quantity = 0
            original_profit = Decimal(0)

        # Handle status change and increment sold count
        if self.pk:
            if original_status != 'Sold' and self.status == 'Sold':
                print("Debug: Status changed to Sold. Incrementing sold count.")
                self.increment_sold_count()
            elif original_status == 'Sold' and self.status != 'Sold':
                print("Debug: Status changed from Sold to Available. Decrementing sold count.")
                self.decrement_sold_count()

        elif self.status == 'Sold':
            print("Debug: New item with status Sold. Incrementing sold count.")
            self.increment_sold_count()

        # Calculate profit considering the quantity
        if self.price_sold and self.price_sold > Decimal(0):
            total_paid = Decimal(self.price_paid) * self.quantity
            total_sold = Decimal(self.price_sold) * self.quantity
            self.profit = total_sold - total_paid
            print(f"Debug: Calculated profit (with quantity): {self.profit}")
        else:
            self.profit = None  # Set profit to None if sale price is 0.00
            print("Debug: Sale price is 0.00 or not set. Profit set to None.")

        super(Inventory, self).save(*args, **kwargs)
        print("Debug: Inventory item saved successfully.")

        # Adjust profit count
        if self.pk and self.profit is not None:
            profile = self.get_profile()
            profile.profit_count -= original_profit  # Subtract the original profit
            profile.profit_count += self.profit  # Add the updated profit
            print(f"Debug: Adjusted profit count by subtracting {original_profit} and adding {self.profit}. New profit count: {profile.profit_count}")
            profile.save()

        # Adjust inventory count if quantity or status has changed
        if self.pk and (self.quantity != original_quantity or self.status != original_status):
            profile = self.get_profile()
            if self.status == 'Available':
                difference = self.quantity - original_quantity
                profile.inventory_count += difference
                print(f"Debug: Adjusted inventory count by {difference}. New inventory count: {profile.inventory_count}")
            elif self.status == 'Sold' and original_status != 'Sold':
                profile.inventory_count -= self.quantity
                print(f"Debug: Sold {self.quantity} items. New inventory count: {profile.inventory_count}")
            profile.save()

    def decrement_sold_count(self):
        profile = self.get_profile()
        profile.sold_count -= self.quantity
        profile.save()

    def increment_sold_count(self):
        profile = self.get_profile()
        profile.sold_count += self.quantity
        profile.save()

    def increment_inventory_count(self):
        profile = self.get_profile()

        if self.status == 'Available':
            # Add items to inventory
            profile.inventory_count += self.quantity
            print(f"Debug: Added {self.quantity} items to inventory. New inventory count: {profile.inventory_count}")
        
        elif self.status == 'Sold':
            # Check if the inventory count is sufficient
            if profile.inventory_count >= self.quantity:
                profile.inventory_count -= self.quantity  # Subtract items from inventory
                print(f"Debug: Sold {self.quantity} items. New inventory count: {profile.inventory_count}")
            else:
                # Edge case: Trying to sell more items than available
                raise ValueError("Attempted to sell more items than available in inventory.")

        profile.save()

    def increment_profit_count(self):
        profile = self.get_profile()
        if self.profit is not None:
            profile.profit_count += self.profit  # Increment the profile's total profit count
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
    secondary_email = models.EmailField(max_length=254, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    profile_pic = models.ImageField(default='profile_pic/default_image.jpg', upload_to='profile_pic/', null=True, blank=True)
    instagram = models.URLField(max_length=200, blank=True)
    inventory_link = models.URLField(max_length=200, blank=True)
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
