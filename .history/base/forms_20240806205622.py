from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import Inventory, Profile, User

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'secondary_email', 'phone_number', 'profile_pic', 'instagram'
        ]
