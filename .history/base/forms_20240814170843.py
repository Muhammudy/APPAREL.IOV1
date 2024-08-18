from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User  # Import User from auth models
from .models import Inventory, Profile, DailyMetrics, MonthlyMetrics, YearlyMetrics

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'
        exclude = ['user']  # Exclude the user field



class CustomUserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['secondary_email', 'phone_number', 'profile_pic', 'instagram', 'inventory_link', 'company_logo']





class DailyMetricsForm(forms.ModelForm):
    class Meta:
        model = DailyMetrics
        fields = ['daily_profit_goal', 'daily_sales_goal', 'daily_inventory_goal']


class MonthlyMetricsForm(forms.ModelForm):
    class Meta:
        model = MonthlyMetrics
        fields = ['monthly_profit_goal', 'monthly_sales_goal', 'monthly_inventory_goal']


class YearlyMetricsForm(forms.ModelForm):
    class Meta:
        model = YearlyMetrics
        fields = ['yearly_profit_goal', 'yearly_sales_goal', 'yearly_inventory_goal']