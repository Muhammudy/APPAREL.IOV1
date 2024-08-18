from django import forms
from .models import Inventory
from .models import Profile
from .models import User
from django.contrib.auth.forms import UserChangeForm

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
        fields = [
            'secondary_email', 'phone_number', 'profile_pic', 'street_address', 
            'city', 'state', 'postal_code', 'country', 'linkedin', 'twitter', 
            'facebook', 'instagram', 'bio', 'birth_date', 'gender'
        ]

