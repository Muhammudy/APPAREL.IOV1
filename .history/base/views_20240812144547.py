from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
import requests
import logging
from .models import Inventory, Profile
from .forms import InventoryForm, CustomUserUpdateForm, ProfileUpdateForm
from .models import DailyMetrics, MonthlyMetrics, YearlyMetrics
from django.utils import timezone


logger = logging.getLogger(__name__)

# Login page view


def calculate_sales_percentage(metrics, total_sales):
    if not metrics or metrics.sold_count == 0 or total_sales == 0:
        return 0
    return (metrics.sold_count / total_sales) * 100

def calculate_inventory_percentage(metrics, total_inventory):
    if not metrics or metrics.inventory_count == 0 or total_inventory == 0:
        return 0
    return (metrics.inventory_count / total_inventory) * 100

def calculate_profit_percentage(metrics, total_profit):
    if not metrics or metrics.profit_count == 0 or total_profit == 0:
        return 0
    return (metrics.profit_count / total_profit) * 100



def loginPage(request):
    page = 'login'

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "User does not exist")
            return redirect('login')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Username or password does not exist")
            return redirect('login')

    context = {'page': page}
    return render(request, 'login.html', context)

# User settings view
@login_required
def settings(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        user_form = CustomUserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('settings')
    else:
        user_form = CustomUserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'settings.html', context)

# Fetch sneaker data view
@login_required
def get_sneaker_data(request):
    keyword = request.GET.get('keyword', 'yeezy slide')
    try:
        response = requests.get(f'http://localhost:4000/get-sneaker-data?keyword={keyword}')
        response.raise_for_status()
        products = response.json()
        return render(request, 'inventory.html', {'products': products, 'keyword': keyword})
    except requests.exceptions.RequestException as e:
        return render(request, 'inventory.html', {'error': str(e), 'keyword': keyword})

# Logout user view
@login_required
def logoutUser(request):
    logout(request)
    return redirect("home")

# Register new user view
def registerPage(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'register.html', {'form': form})

# Home page view
def home(request):
    return render(request, 'home.html')

# Signup page view
def signup(request):
    return render(request, "login.html")

# Dashboard view
@login_required(login_url='login')
def dashboard(request):
    today = timezone.now().date()
    daily_metrics = DailyMetrics.objects.filter(user=request.user, date=today).first()  # Get today's metrics
    monthly_metrics = MonthlyMetrics.objects.filter(user=request.user).order_by('-year', '-month').first()  # Get the latest monthly metrics
    yearly_metrics = YearlyMetrics.objects.filter(user=request.user).order_by('-year').first()  # Get the latest yearly metrics

    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    # Calculate daily totals
    daily_total_sales = daily_metrics.sold_count if daily_metrics else 0
    daily_total_inventory = daily_metrics.inventory_count if daily_metrics else 0
    daily_total_profit = daily_metrics.profit_count if daily_metrics else 0

    # Calculate monthly totals
    monthly_total_sales = monthly_metrics.sold_count if monthly_metrics else 0
    monthly_total_inventory = monthly_metrics.inventory_count if monthly_metrics else 0
    monthly_total_profit = monthly_metrics.profit_count if monthly_metrics else 0

    # Calculate yearly totals
    yearly_total_sales = yearly_metrics.sold_count if yearly_metrics else 0
    yearly_total_inventory = yearly_metrics.inventory_count if yearly_metrics else 0
    yearly_total_profit = yearly_metrics.profit_count if yearly_metrics else 0

    # Calculate daily percentages
    daily_sales_percentage = calculate_sales_percentage(daily_metrics, daily_total_sales)
    daily_inventory_percentage = calculate_inventory_percentage(daily_metrics, daily_total_inventory)
    daily_profit_percentage = calculate_profit_percentage(daily_metrics, daily_total_profit)

    # Calculate monthly percentages
    monthly_sales_percentage = calculate_sales_percentage(monthly_metrics, monthly_total_sales)
    monthly_inventory_percentage = calculate_inventory_percentage(monthly_metrics, monthly_total_inventory)
    monthly_profit_percentage = calculate_profit_percentage(monthly_metrics, monthly_total_profit)

    # Calculate yearly percentages
    yearly_sales_percentage = calculate_sales_percentage(yearly_metrics, yearly_total_sales)
    yearly_inventory_percentage = calculate_inventory_percentage(yearly_metrics, yearly_total_inventory)
    yearly_profit_percentage = calculate_profit_percentage(yearly_metrics, yearly_total_profit)

    if request.method == 'POST':
        user_form = CustomUserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('home')
    else:
        user_form = CustomUserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    inventory_items = Inventory.objects.filter(user=request.user)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'inventory_items': inventory_items,
        'daily_metrics': daily_metrics,
        'monthly_metrics': monthly_metrics,
        'yearly_metrics': yearly_metrics,
        'total_sales': daily_total_sales,
        'total_inventory': daily_total_inventory,
        'total_profit': daily_total_profit,
        'daily_sales_percentage': daily_sales_percentage,
        'daily_inventory_percentage': daily_inventory_percentage,
        'daily_profit_percentage': daily_profit_percentage,
        'monthly_sales_percentage': monthly_sales_percentage,
        'monthly_inventory_percentage': monthly_inventory_percentage,
        'monthly_profit_percentage': monthly_profit_percentage,
        'yearly_sales_percentage': yearly_sales_percentage,
        'yearly_inventory_percentage': yearly_inventory_percentage,
        'yearly_profit_percentage': yearly_profit_percentage,
    }
    return render(request, "dashboard.html", context)




# Inventory view

@login_required(login_url='login')
def inventory(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    # Initialize the forms outside the if-else block
    user_form = CustomUserUpdateForm(instance=request.user)
    profile_form = ProfileUpdateForm(instance=profile)

    if request.method == 'POST':
        form = InventoryForm(request.POST, request.FILES)
        if form.is_valid():
            inventory_item = form.save(commit=False)
            inventory_item.user = request.user  # Ensure the user field is set to the logged-in user
            inventory_item.save()
            return redirect('inventory')
        else:
            print(form.errors)
    else:
        form = InventoryForm()

    inventory_items = Inventory.objects.filter(user=request.user)  # Show only the user's items
    context = {
        'form': form,
        'inventory_items': inventory_items,
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'inventory.html', context)

# Update inventory item view
@login_required(login_url='login')
def updateInventory(request, pk):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    inventory_item = get_object_or_404(Inventory, pk=pk, user=request.user)

    if request.method == 'POST':
        if 'delete' in request.POST:
            inventory_item.delete()
            return redirect('inventory')
        else:
            form = InventoryForm(request.POST, instance=inventory_item)
            if form.is_valid():
                form.save()
                return redirect('inventory')
            else:
                print(form.errors)
    else:
        form = InventoryForm(instance=inventory_item)

    context = {
        'form': form,
        'inventory_item': inventory_item,
    }
    return render(request, 'edit.html', context)

# Delete inventory item view
@login_required(login_url='login')
def deleteInventory(request, pk):
    inventory_item = get_object_or_404(Inventory, pk=pk, user=request.user)
    if request.method == "POST":
        inventory_item.delete()
        return redirect('inventory')
    return render(request, 'delete.html', {'obj': inventory_item})
