from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # روابط التطبيقات
    path('accounts/', include('accounts.urls')),
    path('orders/', include('orders.urls')),
    path('stores/', include('stores.urls')),
    path('delivery/', include('delivery.urls')),
    path('news/', include('news.urls')),
    path('ads/', include('ads.urls')),
    path('', include('core.urls')),  # تأكد أن الصفحة الرئيسية تعمل بشكل سليم
]
