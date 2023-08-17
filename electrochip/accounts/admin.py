from django.contrib import admin

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User  # Import the User model

from electrochip.accounts.forms import EditUserProfileForm, RegisterUserForm

UserModel = get_user_model()


@admin.register(UserModel)
class CustomUserAdmin(UserAdmin):
    form = EditUserProfileForm
    add_form = RegisterUserForm
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_provider', 'is_staff', 'slug',)
    list_filter = ('is_provider', 'is_staff', 'is_superuser', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = (
        ('User', {
            'fields': ('username', 'email', 'password',)
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'profile_picture',)
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)
          }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined',)
        }),
    )
