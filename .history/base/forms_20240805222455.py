from django import forms
from .models import Inventory
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['secondary_email', 'phone_number', 'address']
