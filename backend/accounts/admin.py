from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'role_type', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Info', {'fields': ('role_type', 'phone_number')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
