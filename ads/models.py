from django.db import models
from cloudinary.models import CloudinaryField
from django.utils import timezone

# ✅ إعلان عام
class Advertisement(models.Model):
    title = models.CharField("عنوان الإعلان", max_length=200)
    text = models.TextField("نص الإعلان", blank=True)
    link = models.URLField("رابط خارجي", blank=True)
    image = CloudinaryField("صورة الإعلان")
    is_active = models.BooleanField("مفعل", default=True)
    created_at = models.DateTimeField("تاريخ الإضافة", auto_now_add=True)

    def __str__(self):
        return self.title

# ✅ نافذة ترحيب عند زيارة الموقع لأول مرة في اليوم
from django.db import models

class WelcomePopup(models.Model):
    title = models.CharField("عنوان الرسالة", max_length=200)
    message = models.TextField("محتوى الرسالة")
    image = models.ImageField("الصورة (اختياري)", upload_to="popups/", blank=True, null=True)  # ✅ الحقل الجديد
    is_active = models.BooleanField("مفعل", default=True)
    created_at = models.DateTimeField("تاريخ الإضافة", auto_now_add=True)

    def __str__(self):
        return self.title


# ✅ نافذة منبثقة مخصصة قابلة للتوقيت
class PopupMessage(models.Model):
    title = models.CharField("العنوان", max_length=100)
    content = models.TextField("المحتوى", help_text="يمكنك استخدام HTML مثل <br> للفواصل")
    image = CloudinaryField("الصورة", blank=True, null=True)
    is_active = models.BooleanField("مفعل", default=True)

    start_date = models.DateTimeField("تاريخ البداية", default=timezone.now)
    end_date = models.DateTimeField("تاريخ الانتهاء", blank=True, null=True)

    created_at = models.DateTimeField("تاريخ الإنشاء", auto_now_add=True)

    class Meta:
        verbose_name = "نافذة منبثقة"
        verbose_name_plural = "النوافذ المنبثقة"

    def __str__(self):
        return self.title

    def is_valid_now(self):
        now = timezone.now()
        return self.is_active and self.start_date <= now and (self.end_date is None or now <= self.end_date)
