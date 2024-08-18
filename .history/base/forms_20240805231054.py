from django import forms
from .models import Inventory
from .models import Profile
from .models import User
from django.contrib.auth.forms import UserCreationForm

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'




