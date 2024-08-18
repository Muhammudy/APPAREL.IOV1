from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.utils import timezone

class Inventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    name = models.CharField(max_length=255)
    description = models.TextField(max_length=50, null=True, blank=True)
    sku = models.CharField(default="N/A", max_length=255)
    price_paid = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    price_sold = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    profit = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    size = models.CharField(default="N/A", max_length=10, null=True, blank=True)
    condition = models.CharField(max_length=50, choices=[('New', 'New'), ('Used', 'Used'), ('Lightly Used', 'Lightly Used')])
    quantity = models.PositiveIntegerField(default=1)
    sold_quantity = models.PositiveIntegerField(default=0, editable=False)  # Track sold items separately
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
            profile = self.get_profile()
            original = Inventory.objects.get(pk=self.pk)
            original_status = original.status
            original_quantity = original.quantity
            original_sold_quantity = original.sold_quantity
            print(f"Debug: Original status: {original_status}, New status: {self.status}")

            if original_status != 'Sold' and self.status == 'Sold':
                # Changing to Sold, update sold_quantity
                self.sold_quantity += self.quantity
                print("Debug: Status changed to Sold. Incrementing sold count.")
                profile.inventory_count -= self.quantity
                profile.save()
                self.increment_sold_count()

        elif self.status == 'Sold':
            # New item being marked as Sold
            self.sold_quantity += self.quantity
            print("Debug: New item with status Sold. Incrementing sold count.")
            self.increment_sold_count()

        # Debugging: Check the sale price before calculating profit
        print(f"Debug: Sale price before profit calculation: {self.price_sold}")

        # Calculate profit considering only the sold quantity
        if self.price_sold and self.price_sold > Decimal(0):
            total_paid = Decimal(self.price_paid) * self.sold_quantity
            total_sold = Decimal(self.price_sold) * self.sold_quantity
            self.profit = total_sold - total_paid
            print(f"Debug: Calculated profit (based on sold quantity): {self.profit}")
        else:
            self.profit = None  # Set profit to None if sale price is 0.00
            print("Debug: Sale price is 0.00 or not set. Profit set to None.")

        super(Inventory, self).save(*args, **kwargs)
        print("Debug: Inventory item saved successfully.")

        # Increment the profile's sold count and profit count
        self.increment_profit_count()
        self.increment_inventory_count()
        self.update_daily_metrics()
        self.update_monthly_metrics()
        self.update_yearly_metrics()

    def update_daily_metrics(self):
        profile = self.get_profile()
        today = timezone.now().date()
        daily_metrics, created = DailyMetrics.objects.get_or_create(user=self.user, date=today)
    
        # Update the metrics for the day
        daily_metrics.inventory_count = profile.inventory_count
        daily_metrics.sold_count = profile.sold_count
        daily_metrics.profit_count = profile.profit_count
        
        daily_metrics.save()

    def update_monthly_metrics(self):
        profile = self.get_profile()
        today = timezone.now().date()
        year = today.year
        month = today.month

        monthly_metrics, created = MonthlyMetrics.objects.get_or_create(user=self.user, year=year, month=month)

        # Update the metrics for the month
        monthly_metrics.inventory_count = profile.inventory_count
        monthly_metrics.sold_count = profile.sold_count
        monthly_metrics.profit_count = profile.profit_count
        monthly_metrics.save()

    def update_yearly_metrics(self):
        profile = self.get_profile()
        today = timezone.now().date()
        year = today.year

        yearly_metrics, created = YearlyMetrics.objects.get_or_create(user=self.user, year=year)

        # Update the metrics for the year
        yearly_metrics.inventory_count = profile.inventory_count
        yearly_metrics.sold_count = profile.sold_count
        yearly_metrics.profit_count = profile.profit_count
        
        yearly_metrics.save()

    def increment_sold_count(self):
        profile = self.get_profile()
        profile.sold_count += self.sold_quantity
        profile.save()

    def increment_inventory_count(self):
        profile = self.get_profile()

        if self.pk:  # Check if the item already exists
            original = Inventory.objects.get(pk=self.pk)
            original_status = original.status
        else:
            original_status = None

        if self.status == 'Available':
            # Add items to inventory
            profile.inventory_count += self.quantity
            print(f"Debug: Added {self.quantity} items to inventory. New inventory count: {profile.inventory_count}")

        elif self.status == 'Sold':
            if original_status == 'Available':
                # Subtract items from inventory only if the item was originally available and is now sold
                if profile.inventory_count >= self.quantity:
                    profile.inventory_count -= self.quantity  # Subtract items from inventory
                    print(f"Debug: Sold {self.quantity} items. New inventory count: {profile.inventory_count}")
            else:
                # Handle cases where the item was newly marked as Sold or was already Sold
                print(f"Debug: Item marked as Sold without affecting inventory count.")

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

class DailyMetrics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    daily_profit_goal = models.DecimalField(max_digits=10, decimal_places=2, default=1000, validators=[MinValueValidator(0)])
    daily_sales_goal = models.PositiveIntegerField(default=100)
    daily_inventory_goal = models.PositiveIntegerField(default=100)
    
    inventory_count = models.IntegerField(default=0)
    sold_count = models.IntegerField(default=0)
    profit_count = models.DecimalField(default=0, max_digits=100, decimal_places=2)

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class MonthlyMetrics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()

    monthly_profit_goal = models.DecimalField(max_digits=10, decimal_places=2, default=1000, validators=[MinValueValidator(0)])
    monthly_sales_goal = models.PositiveIntegerField(default=100)
    monthly_inventory_goal = models.PositiveIntegerField(default=100)
    
    inventory_count = models.IntegerField(default=0)
    sold_count = models.IntegerField(default=0)
    profit_count = models.DecimalField(default=0, max_digits=100, decimal_places=2)

    class Meta:
        unique_together = ('user', 'year', 'month')

    def __str__(self):
        return f"{self.user.username} - {self.year}-{self.month:02d}"

class YearlyMetrics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()



    yearly_profit_goal = models.DecimalField(max_digits=10, decimal_places=2, default=1000, validators=[MinValueValidator(0)])
    yearly_sales_goal = models.PositiveIntegerField(default=100)
    yearly_inventory_goal = models.PositiveIntegerField(default=100)




    inventory_count = models.IntegerField(default=0)
    sold_count = models.IntegerField(default=0)
    profit_count = models.DecimalField(default=0, max_digits=100, decimal_places=2)

    class Meta:
        unique_together = ('user', 'year')

    def __str__(self):
        return f"{self.user.username} - {self.year}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    secondary_email = models.EmailField(max_length=254, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    profile_pic = models.ImageField(default='profile_pic/default_image.jpg', upload_to='profile_pic/', null=True, blank=True)
    instagram = models.URLField(max_length=200, blank=True)
    inventory_link = models.URLField(max_length=200, blank=True)
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
