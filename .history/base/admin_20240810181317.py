from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Inventory, Profile
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

admin.site.register( ProfileAdmin)

# Unregister the default UserAdmin
admin.site.unregister(User)

# Register the custom UserAdmin
admin.site.register(User, CustomUserAdmin)

# Register Inventory and Profile separately
admin.site.register(Inventory)
admin.site.register(Profile)
