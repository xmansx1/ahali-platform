from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('معلومات إضافية', {
            'fields': ('user_type', 'phone_number'),
        }),
    )
    list_display = ('username', 'email', 'user_type', 'is_active', 'is_staff')
