from django import forms
from .models import Inventory
from .models import Profile
from .models import User
from django.contrib.auth.forms import UserCreationForm

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'




class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

