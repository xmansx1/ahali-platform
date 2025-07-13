from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Store
from accounts.models import User  # تأكد من المسار الصحيح لنموذج المستخدم

@receiver(post_save, sender=User)
def create_store_for_merchant(sender, instance, created, **kwargs):
    if created and instance.user_type == 'merchant':
        # أنشئ متجرًا فقط إذا لم يكن موجودًا مسبقًا
        Store.objects.get_or_create(user=instance, defaults={
            'name': f'متجر {instance.username}',
            'phone': '',
            'address': '',
            'latitude': 0.0,
            'longitude': 0.0,
        })
