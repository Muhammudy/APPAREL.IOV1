from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
import requests
import logging
from .models import Inventory, Profile, Home
from .forms import InventoryForm, CustomUserUpdateForm, ProfileUpdateForm, DailyMetricsForm, MonthlyMetricsForm, YearlyMetricsForm, HomeForm
from .models import DailyMetrics, MonthlyMetrics, YearlyMetrics
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



logger = logging.getLogger(__name__)

# Login page view
def calculate_sales_percentage(metrics, sales_goal):
    if not metrics or metrics.sold_count == 0 or sales_goal == 0:
        return 0
    return (metrics.sold_count / sales_goal) * 100

def calculate_inventory_percentage(metrics, inventory_goal):
    if not metrics or metrics.inventory_count == 0 or inventory_goal == 0:
        return 0
    return (metrics.inventory_count / inventory_goal) * 100


def calculate_profit_percentage(metrics, profit_goal):
    if not metrics or metrics.profit_count == 0 or profit_goal == 0:
        return 0
    return (metrics.profit_count / profit_goal) * 100


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

@login_required(login_url='login')
def settings(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    today = timezone.now().date()
    daily_metrics, _ = DailyMetrics.objects.get_or_create(user=request.user, date=today)
    month = today.month
    year = today.year
    monthly_metrics, _ = MonthlyMetrics.objects.get_or_create(user=request.user, year=year, month=month)
    yearly_metrics, _ = YearlyMetrics.objects.get_or_create(user=request.user, year=year)

    if request.method == 'POST':
        user_form = CustomUserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        daily_form = DailyMetricsForm(request.POST, instance=daily_metrics)
        monthly_form = MonthlyMetricsForm(request.POST, instance=monthly_metrics)
        yearly_form = YearlyMetricsForm(request.POST, instance=yearly_metrics)

        if user_form.is_valid() and profile_form.is_valid() and daily_form.is_valid() and monthly_form.is_valid() and yearly_form.is_valid():
            user_form.save()
            profile_form.save()
            daily_form.save()
            monthly_form.save()
            yearly_form.save()

            messages.success(request, 'Your profile and goals have been updated successfully!')
            return redirect('settings')
        else:
            # Debugging: print errors if forms are not valid
            print("User Form Errors:", user_form.errors)
            print("Profile Form Errors:", profile_form.errors)
            print("Daily Form Errors:", daily_form.errors)
            print("Monthly Form Errors:", monthly_form.errors)
            print("Yearly Form Errors:", yearly_form.errors)

    else:
        user_form = CustomUserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
        daily_form = DailyMetricsForm(instance=daily_metrics)
        monthly_form = MonthlyMetricsForm(instance=monthly_metrics)
        yearly_form = YearlyMetricsForm(instance=yearly_metrics)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'daily_form': daily_form,
        'monthly_form': monthly_form,
        'yearly_form': yearly_form,
    }

    return render(request, 'settings.html', context)


# Fetch sneaker data view
@login_required(login_url='login')
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
@login_required(login_url='login')
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
    homee = Home.objects.first()  # Fetch the first instance of Home, or you can query in other ways

    context = {'homee': homee}  # Passing the instance in a dictionary
    return render(request, 'home.html', context)

# Signup page view
def signup(request):
    return render(request, "login.html")

# Dashboard view
@login_required(login_url='login')
def dashboard(request):
    today = timezone.now().date()
    user = request.user

    # Get today's daily metrics, latest monthly metrics, and latest yearly metrics
    daily_metrics = DailyMetrics.objects.filter(user=user, date=today).first()
    monthly_metrics = MonthlyMetrics.objects.filter(user=user).order_by('-year', '-month').first()
    yearly_metrics = YearlyMetrics.objects.filter(user=user).order_by('-year').first()

    # Ensure profile exists or create it
    profile, created = Profile.objects.get_or_create(user=user)

    # Set default values for goals and metrics if daily_metrics is None
    daily_sales_goal = daily_inventory_goal = daily_profit_goal = 0
    daily_total_sales = daily_total_inventory = daily_total_profit = 0

    if daily_metrics:
        daily_sales_goal = daily_metrics.daily_sales_goal
        daily_inventory_goal = daily_metrics.daily_inventory_goal
        daily_profit_goal = daily_metrics.daily_profit_goal
        daily_total_sales = daily_metrics.sold_count
        daily_total_inventory = daily_metrics.inventory_count
        daily_total_profit = daily_metrics.profit_count

    # Set default values for monthly metrics
    monthly_total_sales = monthly_total_inventory = monthly_total_profit = 0
    monthly_sales_percentage = monthly_inventory_percentage = monthly_profit_percentage = 0

    if monthly_metrics:
        monthly_total_sales = monthly_metrics.sold_count
        monthly_total_inventory = monthly_metrics.inventory_count
        monthly_total_profit = monthly_metrics.profit_count
        monthly_sales_percentage = calculate_sales_percentage(monthly_metrics, monthly_metrics.monthly_sales_goal)
        monthly_inventory_percentage = calculate_inventory_percentage(monthly_metrics, monthly_metrics.monthly_inventory_goal)
        monthly_profit_percentage = calculate_profit_percentage(monthly_metrics, monthly_metrics.monthly_profit_goal)

    # Set default values for yearly metrics
    yearly_total_sales = yearly_total_inventory = yearly_total_profit = 0
    yearly_sales_percentage = yearly_inventory_percentage = yearly_profit_percentage = 0

    if yearly_metrics:
        yearly_total_sales = yearly_metrics.sold_count
        yearly_total_inventory = yearly_metrics.inventory_count
        yearly_total_profit = yearly_metrics.profit_count
        yearly_sales_percentage = calculate_sales_percentage(yearly_metrics, yearly_metrics.yearly_sales_goal)
        yearly_inventory_percentage = calculate_inventory_percentage(yearly_metrics, yearly_metrics.yearly_inventory_goal)
        yearly_profit_percentage = calculate_profit_percentage(yearly_metrics, yearly_metrics.yearly_profit_goal)

    # Calculate daily percentages with default values of 0% if no data exists
    daily_sales_percentage = calculate_sales_percentage(daily_metrics, daily_sales_goal)
    daily_inventory_percentage = calculate_inventory_percentage(daily_metrics, daily_inventory_goal)
    daily_profit_percentage = calculate_profit_percentage(daily_metrics, daily_profit_goal)

    if request.method == 'POST':
        user_form = CustomUserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('home')
    else:
        user_form = CustomUserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=profile)

    current_theme = request.COOKIES.get('theme', 'light')

    # Prepare the context with the updated theme
    inventory_items = Inventory.objects.filter(user=user)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'inventory_items': inventory_items,
        'daily_metrics': daily_metrics,
        'monthly_metrics': monthly_metrics,
        'yearly_metrics': yearly_metrics,
        'daily_total_sales': daily_total_sales,
        'daily_total_inventory': daily_total_inventory,
        'daily_total_profit': daily_total_profit,
        'daily_sales_percentage': daily_sales_percentage,
        'daily_inventory_percentage': daily_inventory_percentage,
        'daily_profit_percentage': daily_profit_percentage,
        'monthly_total_sales': monthly_total_sales,
        'monthly_total_inventory': monthly_total_inventory,
        'monthly_total_profit': monthly_total_profit,
        'monthly_sales_percentage': monthly_sales_percentage,
        'monthly_inventory_percentage': monthly_inventory_percentage,
        'monthly_profit_percentage': monthly_profit_percentage,
        'yearly_total_sales': yearly_total_sales,
        'yearly_total_inventory': yearly_total_inventory,
        'yearly_total_profit': yearly_total_profit,
        'yearly_sales_percentage': yearly_sales_percentage,
        'yearly_inventory_percentage': yearly_inventory_percentage,
        'yearly_profit_percentage': yearly_profit_percentage,
        'current_theme': current_theme,
    }

    # Create the response object
    response = render(request, "dashboard.html", context)
    
    # Set the theme cookie
    response.set_cookie('theme', current_theme, max_age=30*24*60*60)  # Cookie expires in 30 days
    
    # Return the response
    return response

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

    # The inventory_items variable should be defined before pagination
    inventory_items = Inventory.objects.filter(user=request.user).order_by('status', '-updated')
    # Paginate the inventory items
    paginator = Paginator(inventory_items, 15)  # Show 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'inventory_items': page_obj,  # Pass the paginated items to the template
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
