from django.db import models

class Advertisement(models.Model):
    title = models.CharField("عنوان الإعلان", max_length=200)
    text = models.TextField("نص الإعلان", blank=True)
    link = models.URLField("رابط خارجي", blank=True)
    image = models.ImageField("صورة الإعلان", upload_to="ads/")
    is_active = models.BooleanField("مفعل", default=True)
    created_at = models.DateTimeField("تاريخ الإضافة", auto_now_add=True)  # ✅ الحقل الجديد

    def __str__(self):
        return self.title
