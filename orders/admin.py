# orders/admin.py
from django.contrib import admin
from .models import Order, StoreOrder, Store

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'store', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('customer_name', 'customer_phone')

@admin.register(StoreOrder)
class StoreOrderAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'store', 'order_type', 'created_at')

 