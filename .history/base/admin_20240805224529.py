# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Inventory, Profile
from .forms import CustomUserCreationForm

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles'


# Unregister the default UserAdmin
admin.site.unregister(User)

# Register the custom UserAdmin
admin.site.register(Inventory)
admin.site.register(Profile)
