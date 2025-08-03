from django.shortcuts import render
from ads.models import Advertisement, PopupMessage, WelcomePopup
from django.utils import timezone
from datetime import datetime

def home(request):
    # ✅ جلب الإعلانات العادية
    ads = Advertisement.objects.filter(is_active=True).order_by('-id')[:6]

    # ✅ جلب نافذة منبثقة موقّتة
    now = timezone.now()
    popup = (
        PopupMessage.objects
        .filter(is_active=True, start_date__lte=now)
        .filter(end_date__isnull=True) | PopupMessage.objects.filter(end_date__gte=now)
    ).order_by('-created_at').first()

    # ✅ جلب رسالة الترحيب إذا لم يتم عرضها خلال آخر 5 ساعات
    welcome_popup = WelcomePopup.objects.filter(is_active=True).order_by('-created_at').first()
    show_welcome = False
    if welcome_popup:
        last_seen = request.COOKIES.get('last_welcome_popup')
        if last_seen:
            try:
                last_time = datetime.strptime(last_seen, "%Y-%m-%dT%H:%M:%S")
                if datetime.now() - last_time > timezone.timedelta(hours=5):
                    show_welcome = True
            except Exception:
                show_welcome = True  # في حال كانت القيمة غير صالحة
        else:
            show_welcome = True  # أول زيارة

    # ✅ عرض الصفحة مع البيانات
    response = render(request, 'core/home.html', {
        'ads': ads,
        'popup': popup,
        'welcome_popup': welcome_popup if show_welcome else None,
    })

    # ✅ تعيين الكوكيز لوقت عرض النافذة الترحيبية
    if show_welcome:
        response.set_cookie(
            'last_welcome_popup',
            datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            max_age=5 * 3600  # 5 ساعات
        )

    return response


    
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