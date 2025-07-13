from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.utils.http import urlencode
from django.template.loader import render_to_string
from datetime import datetime

from .models import Order
from accounts.models import User
from stores.models import Store
from .forms import StoreOrderForm


# ===============================
# 🧮 عدادات الطلب حسب الحالة
# ===============================
def get_order_status_counts(user):
    try:
        store = Store.objects.get(user=user)
    except Store.DoesNotExist:
        return {
            'preparing': 0,
            'delivering': 0,
            'delivered': 0,
            'canceled': 0,
            'deleted': 0,
        }

    qs = Order.objects.filter(store=store)
    return {
        'preparing': qs.filter(status='preparing').count(),
        'delivering': qs.filter(status='delivering').count(),
        'delivered': qs.filter(status='delivered').count(),
        'canceled': qs.filter(status='canceled').count(),
        'deleted': qs.filter(status='deleted').count(),
    }


# ===============================
# 🧾 لوحة التاجر الرئيسية
# ===============================
@login_required
def merchant_dashboard(request):
    if request.user.user_type != 'merchant':
        messages.error(request, "أنت لا تملك صلاحية الوصول لهذه الصفحة.")
        return redirect('home')

    try:
        store = Store.objects.get(user=request.user)
    except Store.DoesNotExist:
        messages.error(request, "لم يتم العثور على متجر مرتبط بهذا الحساب.")
        return redirect('home')

    orders = Order.objects.filter(store=store).order_by('-created_at')
    status_counts = get_order_status_counts(request.user)

    return render(request, 'orders/merchant_dashboard.html', {
        'orders': orders,
        'status_counts': status_counts,
        'store': store,
    })


# ===============================
# 🔁 جزء الطلبات (AJAX)
# ===============================
@login_required
def merchant_orders_partial(request):
    if request.user.user_type != 'merchant':
        return JsonResponse({'error': 'غير مصرح'}, status=403)

    try:
        store = Store.objects.get(user=request.user)
    except Store.DoesNotExist:
        return JsonResponse({'error': 'لا يوجد متجر مرتبط بالحساب'}, status=404)

    orders = Order.objects.filter(store=store).exclude(status__in=['delivered', 'canceled', 'deleted']).order_by('-created_at')
    
    return render(request, 'orders/order_list_partial.html', {'orders': orders})


# ===============================
# 📊 عدادات الطلبات (JSON)
# ===============================
@login_required
def merchant_status_counts(request):
    if request.user.user_type != 'merchant':
        return JsonResponse({}, status=403)

    counts = get_order_status_counts(request.user)
    return JsonResponse(counts)


# ===============================
# 🧩 جزء العدادات (AJAX HTML)
# ===============================
@login_required
def merchant_counters_partial(request):
    if request.user.user_type != 'merchant':
        return JsonResponse({}, status=403)

    counts = get_order_status_counts(request.user)
    html = render_to_string('orders/counters_partial.html', {'status_counts': counts})
    return JsonResponse({'html': html, 'counts': counts})


# ===============================
# 🔁 تحديث حالة الطلب
# ===============================
@require_POST
@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    try:
        store = Store.objects.get(user=request.user)
    except Store.DoesNotExist:
        messages.error(request, "لا تملك صلاحية تعديل هذا الطلب.")
        return redirect('merchant_dashboard')

    if order.store != store:
        messages.error(request, "هذا الطلب لا يخص متجرك.")
        return redirect('merchant_dashboard')

    new_status = request.POST.get('status')
    if new_status not in dict(Order.Status.choices):
        messages.error(request, "حالة الطلب غير صالحة.")
        return redirect('merchant_dashboard')

    if new_status == 'delivering':
        amount = request.POST.get('invoice_amount')
        if not amount:
            messages.error(request, "يرجى إدخال مبلغ الفاتورة قبل إرسال الطلب للمندوب.")
            return redirect('merchant_dashboard')
        order.invoice_amount = amount
        order.assigned_to = None

    elif new_status == 'preparing':
        message = (
            f"مرحباً {order.customer_name} 👋\n"
            f"طلبك من متجر {order.store} قيد التجهيز 🛍️\n"
            f"تفاصيل الطلب: {order.details}\n"
            "شكرًا لتسوقك معنا!"
        )
        params = urlencode({'text': message})
        whatsapp_url = f"https://wa.me/{order.customer_phone}?{params}"
        order.status = new_status
        order.save()
        return HttpResponseRedirect(whatsapp_url)

    order.status = new_status
    order.save()
    messages.success(request, "تم تحديث حالة الطلب بنجاح.")
    return redirect('merchant_dashboard')


# ===============================
# 📁 أرشيف الطلبات للتاجر
# ===============================
@login_required
def merchant_archive(request):
    if request.user.user_type != 'merchant':
        return redirect('login')

    try:
        store = Store.objects.get(user=request.user)
    except Store.DoesNotExist:
        return redirect('store_settings')

    orders = Order.objects.filter(
        store=store,
        status__in=['delivered', 'canceled', 'deleted']
    )

    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)

    date = request.GET.get('date')
    if date:
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            orders = orders.filter(created_at__date=date_obj)
        except ValueError:
            pass

    orders = orders.order_by('-created_at')

    return render(request, 'orders/merchant_archive.html', {
        'orders': orders,
        'selected_status': status or '',
        'selected_date': date or ''
    })


# ===============================
# 📄 تفاصيل الطلب (عادي)
# ===============================
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.user != order.store.user and request.user.user_type != 'admin':
        messages.error(request, "غير مصرح لك بعرض هذا الطلب.")
        return redirect('merchant_dashboard')

    return render(request, 'orders/order_detail.html', {'order': order})


# ===============================
# 🪟 تفاصيل الطلب (Modal)
# ===============================
@login_required

def order_detail_ajax(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'orders/order_detail_modal.html', {'order': order})

# ===============================
# 🛒 استقبال طلبات الزوار (POST AJAX)
# ===============================
@require_POST
def create_store_order(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    form = StoreOrderForm(request.POST)

    if form.is_valid():
        order = form.save(commit=False)
        order.store = store
        order.save()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'errors': form.errors}, status=400)


# ===============================
# 🛒 استقبال طلبات الزوار (عبر POST عادي)
# ===============================
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from .models import Order
from stores.models import Store


@csrf_protect
def submit_store_order(request, store_id):
    store = get_object_or_404(Store, id=store_id)

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        phone_number = request.POST.get("phone_number")
        order_details = request.POST.get("order_details")
        order_type = request.POST.get("order_type")
        location_lat = request.POST.get("location_lat")
        location_lng = request.POST.get("location_lng")

        if not all([full_name, phone_number, order_details, order_type]):
            messages.error(request, "يرجى تعبئة جميع الحقول المطلوبة.")
            return redirect('public_store_browser')

        # ✅ محاولة تحويل الإحداثيات إلى float
        try:
            lat = float(location_lat) if location_lat else None
            lng = float(location_lng) if location_lng else None
        except ValueError:
            lat = None
            lng = None

        order = Order.objects.create(
            store=store,
            customer_name=full_name,
            customer_phone=phone_number,
            details=order_details,
            delivery_type=order_type,
            customer_location=f"{location_lat},{location_lng}" if lat and lng else "",
            latitude=lat,
            longitude=lng,
            created_at=timezone.now(),
            status='new'
        )

        messages.success(request, "✅ تم إرسال الطلب بنجاح!")
        return redirect('public_store_browser')

    messages.error(request, "طريقة الطلب غير صحيحة.")
    return redirect('public_store_browser')
# ===============================
# 📊 عدادات الطلبات للمشرف (JSON)
# ===============================
@login_required
def admin_order_status_counts(request):
    if request.user.user_type != 'admin':
        return JsonResponse({}, status=403)

    counts = {
        'preparing': Order.objects.filter(status='preparing').count(),
        'delivering': Order.objects.filter(status='delivering').count(),
        'delivered': Order.objects.filter(status='delivered').count(),
        'canceled': Order.objects.filter(status='canceled').count(),
        'deleted': Order.objects.filter(status='deleted').count(),
    }
    return JsonResponse(counts)
