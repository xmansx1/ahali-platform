from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from orders.models import Order
from .forms import DeliverySettingsForm

# ✅ لوحة المندوب: عرض الطلبات الجاهزة للتوصيل
@login_required
def delivery_dashboard(request):
    if request.user.user_type != 'delivery':
        messages.error(request, "غير مصرح لك بالوصول لهذه الصفحة.")
        return redirect('home')

    # جلب الطلبات المتاحة
    orders = Order.objects.filter(status='delivering', assigned_to__isnull=True).order_by('-created_at')

    if request.method == "POST":
        order_id = request.POST.get("order_id")
        order = get_object_or_404(Order, id=order_id, status='delivering', assigned_to__isnull=True)
        order.assigned_to = request.user
        order.save()
        messages.success(request, "✅ تم تعيينك كمندوب لهذا الطلب.")
        return redirect('delivery_dashboard')

    return render(request, 'delivery/dashboard.html', {'orders': orders})

# ✅ قبول الطلب (ربطه بالمندوب)
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
@login_required
def my_orders(request):
    if request.user.user_type != 'delivery':
        return redirect('login')

    orders = Order.objects.filter(
        status='delivering',
        assigned_to=request.user
    ).order_by('-created_at')

    return render(request, 'delivery/my_orders.html', {'orders': orders})


# ✅ إنهاء الطلب وتحديث حالته
@login_required
def complete_order(request, order_id):
    if request.user.user_type != 'delivery':
        return redirect('login')

    order = get_object_or_404(Order, id=order_id, assigned_to=request.user, status='delivering')
    order.status = 'delivered'
    order.save()
    messages.success(request, "✅ تم تسليم الطلب بنجاح.")
    return redirect('my_orders')
from datetime import datetime

# ✅ أرشيف الطلبات التي تم توصيلها
@login_required
def delivery_archive(request):
    if request.user.user_type != 'delivery':
        return redirect('login')

    orders = Order.objects.filter(
        status='delivered',
        assigned_to=request.user
    )

    # ✅ فلترة اختيارية حسب التاريخ
    date = request.GET.get('date')
    if date:
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            orders = orders.filter(created_at__date=date_obj)
        except ValueError:
            pass

    orders = orders.order_by('-created_at')
    return render(request, 'delivery/archive.html', {
        'orders': orders,
        'selected_date': date or ''
    })


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
                messages.error(request, "❌ تحقق من البيانات.")

    form = DeliverySettingsForm(instance=user)
    return render(request, 'delivery/settings.html', {'form': form})