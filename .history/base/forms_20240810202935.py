from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User  # Import User from auth models
from .models import Inventory, Profile

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'
        exclude = ['user']  # Exclude the user field

    def save(self, commit=True, **kwargs):
        is_inventory_page = kwargs.pop('is_inventory_page', False)
        is_edit_page = kwargs.pop('is_edit_page', False)
        
        inventory = super().save(commit=False)
        if commit:
            inventory.save(is_inventory_page=is_inventory_page, is_edit_page=is_edit_page)
        return inventory

class CustomUserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['secondary_email', 'phone_number', 'profile_pic', 'instagram', 'inventory_link', 'profit_goal', 'sales_goal', 'inventory_goal']
