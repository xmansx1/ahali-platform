from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Advertisement, WelcomePopup, PopupMessage

# ✅ لوحة تحكم الإعلانات العامة
@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'text']

# ✅ لوحة تحكم نافذة الترحيب
@admin.register(WelcomePopup)
class WelcomePopupAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title',)

# ✅ لوحة تحكم النوافذ المنبثقة الموقّتة
@admin.register(PopupMessage)
class PopupMessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'start_date', 'end_date', 'image_preview', 'created_at')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        (None, {
            'fields': (
                'title', 'content', 'image', 'is_active',
                ('start_date', 'end_date'),
            )
        }),
        ('تفاصيل إضافية', {
            'classes': ('collapse',),
            'fields': ('created_at',),
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 80px;" />')
        return "❌ لا توجد صورة"
    
    image_preview.short_description = "معاينة الصورة"
