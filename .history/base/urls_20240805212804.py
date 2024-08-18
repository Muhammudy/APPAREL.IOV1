from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('inventory/', views.inventory, name='inventory'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('dashboard/update/<int:pk>/', views.updateInventory, name='update-inventory'),
    path('dashboard/update/delete/<int:pk>/', views.deleteInventory, name='delete-inventory'),
    path('logout/', views.logoutUser, name='logout'), 
    path('dashboard/', views.dashboard, name='dashboard'),  
    path('settings/', views.settings, name='settings'),  
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)