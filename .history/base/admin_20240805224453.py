    from django.contrib import admin

    from .models import Inventory

    from .models import Profile
    from .models import CustomUserCreationForm

    admin.site.register(Inventory)

    admin.site.register(Profile)

