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
    sold_quantity = models.PositiveIntegerField(default=0, editable=False)
    category = models.CharField(blank=True, default="Sneakers", max_length=50, choices=[('Sneakers', 'Sneakers'), ('Streetwear', 'Streetwear')])
    imageUrl = models.URLField(max_length=200, null=True, blank=True, default='https://example.com/default_image.jpg')
    status = models.CharField(default="Available", max_length=50, choices=[('Sold', 'Sold'), ('Available', 'Available')])
    apparel_size = models.CharField(blank=True, max_length=255, default="N/A")
    image = models.ImageField(default='images/default_image.jpg', upload_to='images/', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['status', '-created']

    def clean(self):
        if self.status == 'Sold' and (self.price_sold is None or self.price_sold <= Decimal(0)):
            raise ValidationError("Price sold must be set and greater than zero when marking an item as Sold.")

    def save(self, *args, **kwargs):
        if self.pk:
            original = Inventory.objects.get(pk=self.pk)
            if original.status == 'Available' and self.status == 'Sold':
                self.handle_sold_item(original)
            elif original.status == 'Sold' and self.status == 'Available':
                self.revert_sold_item(original)
        else:
            if self.status == 'Sold':
                self.handle_sold_item()

        if self.status == 'Available':
            self.increment_inventory_count()
        super(Inventory, self).save(*args, **kwargs)
        self.update_metrics()

    def handle_sold_item(self, original=None):
        self.sold_quantity += self.quantity
        self.update_profile_counts(-self.quantity, self.profit)

    def revert_sold_item(self, original):
        self.sold_quantity -= original.quantity
        self.update_profile_counts(original.quantity, -original.profit)

    def update_profile_counts(self, inventory_change, profit_change):
        profile = self.get_profile()
        profile.inventory_count += inventory_change
        profile.sold_count += self.sold_quantity
        profile.profit_count += profit_change
        profile.save()

    def increment_inventory_count(self):
        profile = self.get_profile()
        profile.inventory_count += self.quantity
        profile.save()

    def update_metrics(self):
        profile = self.get_profile()
        today = timezone.now().date()
        year = today.year
        month = today.month

        # Daily metrics
        daily_metrics, _ = DailyMetrics.objects.get_or_create(user=self.user, date=today)
        daily_metrics.inventory_count = profile.inventory_count
        daily_metrics.sold_count = profile.sold_count
        daily_metrics.profit_count = profile.profit_count
        daily_metrics.save()

        # Monthly metrics
        monthly_metrics, _ = MonthlyMetrics.objects.get_or_create(user=self.user, year=year, month=month)
        monthly_metrics.inventory_count = profile.inventory_count
        monthly_metrics.sold_count = profile.sold_count
        monthly_metrics.profit_count = profile.profit_count
        monthly_metrics.save()

        # Yearly metrics
        yearly_metrics, _ = YearlyMetrics.objects.get_or_create(user=self.user, year=year)
        yearly_metrics.inventory_count = profile.inventory_count
        yearly_metrics.sold_count = profile.sold_count
        yearly_metrics.profit_count = profile.profit_count
        yearly_metrics.save()

    def delete(self, *args, **kwargs):
        profile = self.get_profile()
        if self.status == 'Available':
            profile.inventory_count -= self.quantity
        elif self.status == 'Sold':
            profile.sold_count -= self.sold_quantity
            profile.profit_count -= self.profit

        profile.save()
        super(Inventory, self).delete(*args, **kwargs)
        self.update_metrics()

    def get_profile(self):
        return Profile.objects.get(user=self.user)

    def __str__(self):
        return self.name


class DailyMetrics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    daily_profit_goal = models.DecimalField(max_digits=10, decimal_places=2, default=100, validators=[MinValueValidator(0)])
    daily_sales_goal = models.PositiveIntegerField(default=10)
    daily_inventory_goal = models.PositiveIntegerField(default=50)
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
    monthly_profit_goal = models.DecimalField(max_digits=10, decimal_places=2, default=3000, validators=[MinValueValidator(0)])
    monthly_sales_goal = models.PositiveIntegerField(default=300)
    monthly_inventory_goal = models.PositiveIntegerField(default=1500)
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
    yearly_profit_goal = models.DecimalField(max_digits=10, decimal_places=2, default=36000, validators=[MinValueValidator(0)])
    yearly_sales_goal = models.PositiveIntegerField(default=3600)
    yearly_inventory_goal = models.PositiveIntegerField(default=18000)
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
    sold_count = models.IntegerField(default=0, editable=False)
    inventory_count = models.IntegerField(default=0, editable=False)
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
