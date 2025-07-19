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

    # ✅ مبلغ التوصيل الكامل
    delivery_fee = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=10.0,
        verbose_name="مبلغ التوصيل (ريال)"
    )

    # ✅ نسبة يتحملها العميل من مبلغ التوصيل (0 - 100)
    customer_delivery_share = models.PositiveIntegerField(
        default=100,
        verbose_name="نسبة يتحملها العميل من التوصيل (%)",
        help_text="قيمة من 0 إلى 100. تحدد كم يتحمل العميل من رسوم التوصيل."
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")

    def __str__(self):
        return self.name or (self.user.get_full_name() or self.user.username)

    @property
    def customer_delivery_fee(self):
        """
        تُعيد قيمة التوصيل التي يتحملها العميل فقط.
        يتم تقريبها لأقرب عدد صحيح.
        """
        try:
            if self.delivery_fee is not None and self.customer_delivery_share is not None:
                return int(float(self.delivery_fee) * float(self.customer_delivery_share) / 100)
        except (TypeError, ValueError):
            pass
        return 0
