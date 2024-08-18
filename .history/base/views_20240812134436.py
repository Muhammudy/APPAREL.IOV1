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

logger = logging.getLogger(__name__)

# Login page view
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
    daily_metrics = DailyMetrics.objects.filter(user=request.user).order_by('-date')
    monthly_metrics = MonthlyMetrics.objects.filter(user=request.user).order_by('-year', '-month')
    yearly_metrics = YearlyMetrics.objects.filter(user=request.user).order_by('-year')
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
            return redirect('home')
    else:
        user_form = CustomUserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    inventory_items = Inventory.objects.filter(user=request.user)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'inventory_items': inventory_items,
        'daily_metrics' : daily_metrics,
        'monthly_metrics': monthly_metrics,
        'yearly_metrics': yearly_metrics
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
