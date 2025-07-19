from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from orders.models import Order
from .forms import DeliverySettingsForm
from datetime import datetime

# ✅ لوحة المندوب: عرض الطلبات الجاهزة للتوصيل
@login_required
def delivery_dashboard(request):
    if request.user.user_type != 'delivery':
        messages.error(request, "غير مصرح لك بالوصول لهذه الصفحة.")
        return redirect('home')

    # جلب الطلبات غير المسندة الجاهزة للتوصيل
    orders = Order.objects.filter(status='delivering', assigned_to__isnull=True).order_by('-created_at')

    if request.method == "POST":
        order_id = request.POST.get("order_id")
        order = get_object_or_404(Order, id=order_id, status='delivering', assigned_to__isnull=True)
        order.assigned_to = request.user
        order.save()
        messages.success(request, "✅ تم تعيينك كمندوب لهذا الطلب.")
        return redirect('delivery_dashboard')

    return render(request, 'delivery/dashboard.html', {'orders': orders})

# ✅ قبول الطلب
@login_required
def accept_order(request, order_id):
    if request.user.user_type != 'delivery':
        return redirect('login')

    order = get_object_or_404(Order, id=order_id, status='delivering', assigned_to__isnull=True)
    order.assigned_to = request.user
    order.save()
    messages.success(request, "✅ تم استلام الطلب بنجاح.")
    return redirect('delivery_dashboard')

# ✅ عرض الطلبات المسندة لهذا المندوب
# ✅ عرض الطلبات المسندة لهذا المندوب
@login_required
def my_orders(request):
    if request.user.user_type != 'delivery':
        return redirect('login')

    orders = (
        Order.objects.filter(
            assigned_to=request.user,
            status='delivering'
        )
        .select_related('store', 'store__user')  # ✅ تحميل بيانات المتجر والتاجر المرتبط لتحسين الأداء ومنع أخطاء القالب
        .order_by('-created_at')
    )

    return render(request, 'delivery/my_orders.html', {'orders': orders})

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from orders.models import DeliveryPayment
from orders.models import Order

def pay_delivery_fee(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # ✅ تحقق من أن الطلب يحتوي على مندوب معيّن
    if not order.assigned_to:
        messages.error(request, "لا يمكن تسجيل الدفع بدون وجود مندوب معين لهذا الطلب.")
        return redirect('merchant_orders')  # أو اسم العرض المناسب

    # ✅ تحقق من عدم وجود دفع مسبق
    if hasattr(order, 'delivery_payment'):
        messages.warning(request, "تم دفع مستحقات هذا الطلب مسبقاً.")
        return redirect('merchant_orders')

    if request.method == "POST":
        payment_method = request.POST.get("payment_method")

        if payment_method not in ["cash", "transfer"]:
            messages.error(request, "يرجى تحديد طريقة دفع صحيحة.")
            return redirect('merchant_orders')

        DeliveryPayment.objects.create(
            order=order,
            paid_by=request.user,
            paid_to=order.assigned_to,
            amount=order.delivery_fee,  # ✅ استخدام مبلغ التوصيل مباشرة
            payment_method=payment_method,
            paid_at=timezone.now()
        )

        messages.success(request, "✅ تم تسجيل دفع مستحقات المندوب بنجاح.")
        return redirect('merchant_orders')

    messages.error(request, "طلب غير صالح.")
    return redirect('merchant_orders')


# ✅ إنهاء الطلب
@login_required
def complete_order(request, order_id):
    if request.user.user_type != 'delivery':
        return redirect('login')

    order = get_object_or_404(Order, id=order_id, assigned_to=request.user, status='delivering')
    order.status = 'delivered'
    order.save()
    messages.success(request, "✅ تم تسليم الطلب بنجاح.")
    return redirect('my_orders')

# ✅ أرشيف الطلبات التي تم تسليمها
@login_required
def delivery_archive(request):
    if request.user.user_type != 'delivery':
        return redirect('login')

    orders = Order.objects.filter(status='delivered', assigned_to=request.user)

    # فلترة بالتاريخ (من - إلى)
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    try:
        if date_from:
            orders = orders.filter(created_at__date__gte=datetime.strptime(date_from, "%Y-%m-%d"))
        if date_to:
            orders = orders.filter(created_at__date__lte=datetime.strptime(date_to, "%Y-%m-%d"))
    except ValueError:
        messages.error(request, "صيغة التاريخ غير صحيحة.")

    orders = orders.order_by('-created_at')
    return render(request, 'delivery/archive.html', {
        'orders': orders,
        'date_from': date_from or '',
        'date_to': date_to or ''
    })

# ✅ إعدادات المندوب
@login_required
def delivery_settings(request):
    if request.user.user_type != 'delivery':
        messages.error(request, "غير مصرح لك.")
        return redirect('home')

    user = request.user

    if request.method == "POST":
        if 'save_settings' in request.POST:
            form = DeliverySettingsForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "✅ تم تحديث البيانات بنجاح.")
        elif 'change_password' in request.POST:
            old = request.POST.get("old_password")
            new = request.POST.get("new_password")
            confirm = request.POST.get("confirm_password")
            if new == confirm and user.check_password(old):
                user.set_password(new)
                user.save()
                messages.success(request, "🔐 تم تغيير كلمة المرور.")
            else:
                messages.error(request, "❌ تحقق من صحة كلمة المرور الحالية وتطابق الجديدة.")

    form = DeliverySettingsForm(instance=user)
    return render(request, 'delivery/settings.html', {'form': form})

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from orders.models import Order, DeliveryPayment

from django.db.models import Sum

@login_required
def delivery_earnings(request):
    user = request.user

    # ✅ الطلبات التي تم توصيلها ولم يتم دفعها بعد
    unpaid_orders = Order.objects.filter(
        assigned_to=user,
        status='delivered',
        delivery_payment__isnull=True
    ).select_related('store')

    # ✅ المدفوعات التي تم استلامها
    payments = DeliveryPayment.objects.filter(paid_to=user).select_related('order__store')

    # ✅ المجموع المدفوع من سجل المدفوعات
    total_paid = payments.aggregate(total=Sum('amount'))['total'] or 0

    # ✅ المجموع الغير مدفوع بناء على delivery_fee لكل طلب
    total_unpaid = unpaid_orders.aggregate(total=Sum('delivery_fee'))['total'] or 0

    # ✅ المتاجر التي لم تدفع بعد
    unpaid_stores = unpaid_orders.values('store__name').distinct()

    context = {
        'unpaid_orders': unpaid_orders,
        'payments': payments,
        'total_paid': total_paid,
        'total_unpaid': total_unpaid,
        'unpaid_stores': unpaid_stores,
    }
    return render(request, 'delivery/earnings.html', context)
