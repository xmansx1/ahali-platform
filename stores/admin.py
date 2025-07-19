from django.contrib import admin
from .models import Store

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'store_type', 'is_active', 'is_available', 'created_at')
    list_filter = ('is_active', 'store_type')
    search_fields = ('name', 'phone', 'address')
    readonly_fields = ('created_at',)

    # ترتيب الحقول عند التعديل
    fields = (
        'name',
        'phone',
        'address',
        'latitude',
        'longitude',
        'store_type',
        'is_active',
        'is_available',
        'delivery_fee',
        'free_delivery_min',
        'delivery_policy_note',  # ✅ تمت إضافته هنا
        'created_at',
    )
