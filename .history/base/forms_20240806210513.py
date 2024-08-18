from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import Inventory, Profile, User
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'


class CustomUserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['secondary_email', 'phone_number', 'profile_pic', 'instagram', 'Inventory_link']