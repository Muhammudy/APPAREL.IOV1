from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('inventory/', views.inventory, name='inventory'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('dashboard/update/<int:pk>/', views.updateInventory, name='update-inventory'),
    path('dashboard/update/delete/<int:pk>/', views.deleteInventory, name='delete-inventory'),
    path('logout/', views.logoutUser, name='logout'), 
    path('dashboard/', views.dashboard, name='dashboard'),  
]