from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# Authentication related paths
auth_patterns = [
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
]

# Dashboard related paths
dashboard_patterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/inventory/', views.inventory, name='inventory'),
    path('dashboard/update/<int:pk>/', views.updateInventory, name='update-inventory'),
    path('dashboard/update/delete/<int:pk>/', views.deleteInventory, name='delete-inventory'),
]

# Settings related path
settings_patterns = [
    path('dashboard/settings/', views.settings, name='settings'),
]

# Root and static paths
urlpatterns = [
    path('', views.home, name='home'),
    *auth_patterns,
    *dashboard_patterns,
    *settings_patterns,
     re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
