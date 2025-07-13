from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class UserType(models.TextChoices):
        ADMIN = 'admin', 'مشرف'
        MERCHANT = 'merchant', 'تاجر'
        DELIVERY = 'delivery', 'مندوب'

    user_type = models.CharField(
        "نوع المستخدم",
        max_length=10,
        choices=UserType.choices,
        default=UserType.MERCHANT
    )

    phone_number = models.CharField("رقم الجوال", max_length=15, blank=True)
    is_active = models.BooleanField("حالة التفعيل", default=True)

    # 🏪 خاص بالتجار فقط
    is_available = models.BooleanField("نشاط المتجر", default=True)
    store_location = models.CharField("عنوان المتجر (نص)", max_length=255, null=True, blank=True)
    store_latitude = models.FloatField("خط العرض", null=True, blank=True)
    store_longitude = models.FloatField("خط الطول", null=True, blank=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_user_type_display()})"

    def full_store_address(self):
        if self.store_location and self.store_latitude and self.store_longitude:
            return f"{self.store_location} ({self.store_latitude}, {self.store_longitude})"
        elif self.store_location:
            return self.store_location
        return "موقع غير محدد"
