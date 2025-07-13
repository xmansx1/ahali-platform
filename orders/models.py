from django.db import models
from django.conf import settings
from stores.models import Store


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', 'جديد'
        PREPARING = 'preparing', 'قيد التجهيز'
        DELIVERING = 'delivering', 'قيد التوصيل'
        DELIVERED = 'delivered', 'تم التسليم'
        CANCELED = 'canceled', 'ملغي'
        DELETED = 'deleted', 'محذوف'

    class DeliveryType(models.TextChoices):
        PICKUP = 'pickup', 'استلام من المحل'
        DELIVERY = 'delivery', 'توصيل'

    # ✅ المتجر المرتبط بالطلب
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="direct_orders",
        verbose_name="المتجر"
    )

    # ✅ بيانات العميل
    customer_name = models.CharField("اسم العميل", max_length=100)
    customer_phone = models.CharField("رقم الجوال", max_length=20)
    customer_location = models.CharField("الوصف النصي للموقع", max_length=255, blank=True)
    latitude = models.FloatField("خط العرض", null=True, blank=True)
    longitude = models.FloatField("خط الطول", null=True, blank=True)

    # ✅ تفاصيل الطلب
    details = models.TextField("تفاصيل الطلب")
    notes = models.TextField("ملاحظات إضافية", blank=True)

    # ✅ نوع الطلب (توصيل أو استلام)
    delivery_type = models.CharField(
        "نوع الطلب",
        max_length=20,
        choices=DeliveryType.choices
    )

    # ✅ حالة الطلب
    status = models.CharField(
        "الحالة",
        max_length=20,
        choices=Status.choices,
        default=Status.NEW
    )

    # ✅ ربط الطلب بمندوب التوصيل
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_orders',
        limit_choices_to={'user_type': 'delivery'},
        verbose_name="المندوب"
    )

    created_at = models.DateTimeField("وقت الإنشاء", auto_now_add=True)

    def __str__(self):
        return f"طلب - {self.customer_name} - {self.get_status_display()}"

    class Meta:
        verbose_name = "طلب"
        verbose_name_plural = "الطلبات"
        ordering = ['-created_at']

    # ✅ خصائص للوصول للإحداثيات بسهولة في القالب
    @property
    def customer_latitude(self):
        return self.latitude

    @property
    def customer_longitude(self):
        return self.longitude

    @property
    def store_latitude(self):
        return self.store.latitude if self.store and self.store.latitude else None

    @property
    def store_longitude(self):
        return self.store.longitude if self.store and self.store.longitude else None


class StoreOrder(models.Model):
    ORDER_TYPES = [
        ('pickup', 'استلام من المحل'),
        ('delivery', 'توصيل'),
    ]

    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="store_orders",  # ✅ اسم مختلف لمنع التعارض
        verbose_name="المتجر"
    )
    full_name = models.CharField(max_length=100, verbose_name="الاسم الكامل")
    phone_number = models.CharField(max_length=15, verbose_name="رقم الجوال")
    order_details = models.TextField(verbose_name="تفاصيل الطلب")
    order_type = models.CharField(max_length=20, choices=ORDER_TYPES, verbose_name="نوع الطلب")
    location_lat = models.FloatField(verbose_name="خط العرض")
    location_lng = models.FloatField(verbose_name="خط الطول")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الطلب")

    def __str__(self):
        return f"{self.full_name} - {self.store.name}"

    class Meta:
        verbose_name = "طلب متجر"
        verbose_name_plural = "طلبات المتاجر"
        ordering = ['-created_at']
