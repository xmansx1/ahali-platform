from django.contrib import admin
from .models import Store

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'store_type', 'is_active','is_available', 'created_at')
    list_filter = ('is_active', 'store_type')
    search_fields = ('name', 'phone', 'address')
    readonly_fields = ('created_at',)