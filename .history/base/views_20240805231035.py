from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .models import Inventory
from .forms import InventoryForm
import requests
from django.http import JsonResponse
import logging

# Create your views here.


def loginPage(request):
    page = 'login'



    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "User does not exist")
            return redirect('login')  # Redirect to the login page to display the error

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Use a named URL pattern for redirect
        else:
            messages.error(request, "Username or password does not exist")
            return redirect('login')  # Redirect to the login page to display the error

    context = {'page': page}
    return render(request, 'login.html', context)


def settings(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()

            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('settings')
    else:
        user_form = UserCreationForm(instance=request.user)
        

    context = {
        'user_form': user_form,
    }

    return render(request, 'settings.html', context)










def get_sneaker_data(request):
    keyword = request.GET.get('keyword', 'yeezy slide')
    try:
        response = requests.get(f'http://localhost:4000/get-sneaker-data?keyword={keyword}')
        response.raise_for_status()
        products = response.json()
        return render(request, 'inventory.html', {'products': products, 'keyword': keyword})
    except requests.exceptions.RequestException as e:
        return render(request, 'inventory.html', {'error': str(e), 'keyword': keyword})

def logoutUser(request):
    logout(request)
    return redirect("home")


def registerPage(request):
    form = UserCreationForm()

    if request.method =="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    return render(request, 'register.html', {'form': form})






def home(request):
    return render(request, 'home.html')

def signup(request):
    return render(request, "login.html")


@login_required(login_url = 'login')
def dashboard(request):
    return render(request, "dashboard.html")





logger = logging.getLogger(__name__)

@login_required(login_url='login')
def inventory(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST, request.FILES)  # This line ensures file uploads are handled
        if form.is_valid():
            form.save()
            return redirect('inventory')  # Redirect to the inventory to see the new data
        else:
            print(form.errors)  # For debugging, print form errors to the console
    else:
        form = InventoryForm()

    inventory_items = Inventory.objects.all()
    context = {
        'form': form,
        'inventory_items': inventory_items,
    }
    return render(request, 'inventory.html', context)













def inventory_view(request):
    if request.method == 'POST':
        info = request.POST.get('info')
        category = request.POST.get('category')  # Add category to the payload

        # Prepare the payload to send to the Node.js API
        payload = {
            'info': info,
            'category': category
        }

        # Send the POST request to the Node.js API
        response = requests.post('http://localhost:4000/get-sneaker-data', json=payload)

        # Handle the response from the Node.js API
        if response.status_code == 200:
            data = response.json()
            # Do something with the data received from the Node.js API
            return JsonResponse(data)
        else:
            # Handle error
            return JsonResponse({'error': 'Failed to fetch data from API'}, status=500)

    form = InventoryForm()
    inventory_items = Inventory.objects.all()

    context = {
        'form': form,
        'inventory_items': inventory_items,
    }

    return render(request, 'inventory.html', context)














@login_required(login_url='login')
def updateInventory(request, pk):
    inventory_item = get_object_or_404(Inventory, pk=pk)

    if request.method == 'POST':
        if 'delete' in request.POST:  # Check if the delete button was pressed
            inventory_item.delete()
            return redirect('inventory')
        else:
            form = InventoryForm(request.POST, instance=inventory_item)
            if form.is_valid():
                form.save()  # Save the form before redirecting
                return redirect('inventory')  # Redirect to the inventory page
            else:
                print(form.errors)  # Print form errors for debugging
    else:
        form = InventoryForm(instance=inventory_item)

    context = {
        'form': form,
        'inventory_item': inventory_item,
    }
    return render(request, 'edit.html', context)



@login_required(login_url = 'login')
def deleteInventory(request, pk):
    inventory_item = get_object_or_404(Inventory, pk=pk)
    if request.method == "POST":
        inventory_item.delete()
        return redirect('inventory')
    return render(request, 'delete.html', {'obj': inventory_item})
