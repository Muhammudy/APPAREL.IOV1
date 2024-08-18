from django import forms
from .models import Inventory
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['secondary_email', 'phone_number', 'address']
