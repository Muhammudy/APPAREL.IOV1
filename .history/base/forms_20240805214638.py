from django import forms
from .models import Inventory
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
