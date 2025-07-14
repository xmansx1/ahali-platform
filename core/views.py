from django.shortcuts import render
from ads.models import Advertisement

def home(request):
    ads = Advertisement.objects.filter(is_active=True).order_by('-id')[:6]

    return render(request, 'core/home.html', {
        'ads': ads
    })
    
    
from django.shortcuts import render
from django.db.models import Q
from stores.models import Store  # تأكد من الاستيراد

def public_store_browser(request):
    query = request.GET.get("q", "")
    
    # فلترة المتاجر النشطة والمتاحة فقط
    stores = Store.objects.filter(is_active=True, is_available=True)

    if query:
        # دمج شروط البحث في الاسم أو العنوان
        stores = stores.filter(Q(name__icontains=query) | Q(address__icontains=query))

    return render(request, "public/store_browser.html", {
        "stores": stores,
    })
