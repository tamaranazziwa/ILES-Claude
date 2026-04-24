from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  # special admin class for user models
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),  # add role field to existing user edit form
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role', {'fields': ('role',)}),  # add role field to new user creation form
    )

admin.site.register(CustomUser, CustomUserAdmin)  # show model in admin panel with custom admin class
# Register your models here.
