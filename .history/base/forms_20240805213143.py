from django import forms
from .models import Inventory
from django.contrib.auth.models import User

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
