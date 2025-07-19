from django.shortcuts import render
from ads.models import Advertisement, PopupMessage
from django.utils import timezone

def home(request):
    # ✅ جلب الإعلانات العادية
    ads = Advertisement.objects.filter(is_active=True).order_by('-id')[:6]

    # ✅ جلب نافذة منبثقة صالحة
    now = timezone.now()
    popup = (
        PopupMessage.objects
        .filter(is_active=True, start_date__lte=now)
        .filter(end_date__isnull=True) | PopupMessage.objects.filter(end_date__gte=now)
    ).order_by('-created_at').first()

    return render(request, 'core/home.html', {
        'ads': ads,
        'popup': popup
    })

    
from django.shortcuts import render
from django.db.models import Q
from stores.models import Store  # تأكد من الاستيراد

def public_store_browser(request):
    query = request.GET.get("q", "")
    store_type = request.GET.get("type", "")

    # فلترة المتاجر النشطة والمتاحة فقط
    stores = Store.objects.filter(is_active=True, is_available=True)

    if query:
        stores = stores.filter(Q(name__icontains=query) | Q(address__icontains=query))

    if store_type:
        stores = stores.filter(store_type=store_type)

    # ✅ جلب أنواع المتاجر من choices في الموديل
    store_types = Store.STORE_TYPES


    return render(request, "public/store_browser.html", {
        "stores": stores,
        "store_types": store_types,
    })