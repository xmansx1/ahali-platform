from django.db import models
from accounts.models import User

class Store(models.Model):
    STORE_TYPES = [
        ('grocery', 'بقالة'),
        ('pharmacy', 'صيدلية'),
        ('restaurant', 'مطعم'),
        ('sweets', 'حلويات'),
        ('bakery', 'مخبوزات'),
        ('services', 'سباكة و كهرباء'),
        ('produce', 'خضار و فواكه'),
        ('gifts', 'هدايا'),
        ('coffee', 'كوفي'),
        ('other', 'أخرى'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='store',
        verbose_name="صاحب المتجر"
    )

    name = models.CharField(max_length=255, verbose_name="اسم المتجر", blank=True)
    phone = models.CharField(max_length=15, verbose_name="رقم الجوال", blank=True)
    address = models.TextField(verbose_name="العنوان التفصيلي", blank=True)
    latitude = models.FloatField(verbose_name="خط العرض", null=True, blank=True)
    longitude = models.FloatField(verbose_name="خط الطول", null=True, blank=True)
    store_type = models.CharField(
        max_length=20,
        choices=STORE_TYPES,
        default='other',
        verbose_name="نوع المتجر"
    )
    is_active = models.BooleanField(default=True, verbose_name="نشط؟")
    is_available = models.BooleanField(default=True, verbose_name="متاح لاستقبال الطلبات؟")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")

    def __str__(self):
        return self.name or f"متجر {self.user.get_full_name() or self.user.username}"
