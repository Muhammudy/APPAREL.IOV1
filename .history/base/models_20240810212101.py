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
        is_inventory_page = kwargs.pop('is_inventory_page', False)
        is_edit_page = kwargs.pop('is_edit_page', False)

        if self.pk:
            print(f"Debug: Saving inventory item with ID {self.pk}")
            original_status = Inventory.objects.get(pk=self.pk).status
            print(f"Debug: Original status: {original_status}, New status: {self.status}")

            if original_status != 'Sold' and self.status == 'Sold':
                print("Debug: Status changed to Sold. Incrementing sold count.")
                self.increment_sold_count()
        elif not self.pk and self.status == 'Sold':
            print("Debug: New item with status Sold. Incrementing sold count.")
            self.increment_sold_count()

        # Debugging: Check the sale price before calculating profit
        print(f"Debug: Sale price before profit calculation: {self.price_sold}")

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

        # Increment the profile's sold count and profit count
        self.increment_profit_count()
        self.increment_inventory_count(is_inventory_page=is_inventory_page, is_edit_page=is_edit_page)

    def increment_profit_count(self):
        profile = self.get_profile()

        if self.pk:  # Check if the instance already exists
            original = Inventory.objects.get(pk=self.pk)
            if original.status == 'Sold' and self.status == 'Sold':
                # Subtract the original profit before adding the new one
                profile.profit_count -= original.profit or Decimal(0)
                print(f"Debug: Subtracted original profit of {original.profit}. New profit count: {profile.profit_count}")
        
        if self.profit is not None:
            profile.profit_count += self.profit  # Add the updated profit
            print(f"Debug: Incremented profit by {self.profit}. New profit count: {profile.profit_count}")

        profile.save()

    
    
    def increment_sold_count(self):
        profile = self.get_profile()
        profile.sold_count += self.quantity
        profile.save()

    def increment_inventory_count(self, is_inventory_page=False, is_edit_page=False):
        profile = self.get_profile()

        if self.pk:  # This means the item already exists
            original_quantity = Inventory.objects.get(pk=self.pk).quantity
        else:
            original_quantity = 0  # For new items, the original quantity is 0

        if is_inventory_page:
            # Add items to inventory
            profile.inventory_count += self.quantity
            print(f"Debug: Added {self.quantity} items to inventory. New inventory count: {profile.inventory_count}")

        elif is_edit_page:
            # Compare the current quantity with the original quantity
            if self.quantity > original_quantity:
                difference = self.quantity - original_quantity
                profile.inventory_count += difference
                print(f"Debug: Increased inventory count by {difference}. New inventory count: {profile.inventory_count}")
            elif self.quantity < original_quantity:
                difference = original_quantity - self.quantity
                profile.inventory_count -= difference
                print(f"Debug: Decreased inventory count by {difference}. New inventory count: {profile.inventory_count}")

        elif self.status == 'Sold':
            # Check if the inventory count is sufficient
            if profile.inventory_count >= self.quantity:
                profile.inventory_count -= self.quantity  # Subtract items from inventory
                print(f"Debug: Sold {self.quantity} items. New inventory count: {profile.inventory_count}")
            else:
                # Edge case: Trying to sell more items than available
                print("Warning: Attempted to sell more items than available in inventory. No changes made.")
                # You can raise an exception or handle this scenario appropriately here

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
