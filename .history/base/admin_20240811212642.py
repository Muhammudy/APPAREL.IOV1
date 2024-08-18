from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Inventory, Profile
from .models import DailyMetrics, MonthlyMetrics, YearlyMetrics
from .forms import CustomUserUpdateForm

class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserUpdateForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('sold_count', 'inventory_count', 'profit_count')

@admin.register(DailyMetrics)
class DailyMetricsAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'date', 'inventory_count', 'sold_count', 'profit_count')

@admin.register(MonthlyMetrics)
class MonthlyMetricsAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'year', 'month', 'inventory_count', 'sold_count', 'profit_count')

@admin.register(YearlyMetrics)
class YearlyMetricsAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'year', 'inventory_count', 'sold_count', 'profit_count')

# Unregister the default UserAdmin
admin.site.unregister(User)

# Register the custom UserAdmin
admin.site.register(User, CustomUserAdmin)

# Register Inventory and Profile with their respective admins
admin.site.register(Inventory)
admin.site.register(Profile, ProfileAdmin)
