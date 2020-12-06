from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

class CustomUserAdmin(UserAdmin):
    readonly_fields = ('joined_at',)
    list_display = ('first_name', 'last_name', 'email', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        ('Personal info', {
            'fields': (('first_name', 'last_name'), 'email', 'password')
        }),
        ('Permissions', {
            'fields': ('is_verified', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'joined_at')
        })
    )
    ordering = ['first_name']
    

admin.site.register(User, CustomUserAdmin)
