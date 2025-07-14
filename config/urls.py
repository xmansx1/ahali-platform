from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    # روابط التطبيقات
    path('accounts/', include('accounts.urls')),
    path('orders/', include('orders.urls')),
    path('stores/', include('stores.urls')),
    path('delivery/', include('delivery.urls')),
    path('news/', include('news.urls')),
    path('ads/', include('ads.urls')),  # ✅ هذا هو الصحيح فقط

    path('', include('core.urls')),  # تأكد أن الصفحة الرئيسية تعمل بشكل سليم
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)