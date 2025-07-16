from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from stores.models import Store
from stores.forms import StoreSettingsForm, PasswordChangeForm


@login_required
def store_settings(request):
    user = request.user

    if user.user_type != 'merchant':
        messages.error(request, "🚫 غير مصرح لك بالوصول لهذه الصفحة.")
        return redirect('home')

    try:
        store = user.store
    except Store.DoesNotExist:
        messages.error(request, "❌ لم يتم ربط المستخدم بمتجر.")
        return redirect('home')

    form = StoreSettingsForm(instance=store)
    pass_form = PasswordChangeForm()

    if request.method == 'POST':
        # ✅ حفظ إعدادات المتجر
        if 'save_settings' in request.POST:
            form = StoreSettingsForm(request.POST, instance=store)
            if form.is_valid():
                store_instance = form.save(commit=False)

                # ✅ نحافظ على حالة التفعيل كما كانت
                store_instance.is_active = store.is_active

                store_instance.save()
                messages.success(request, "✅ تم تحديث بيانات المتجر بنجاح.")
                return redirect('store_settings')
            else:
                messages.error(request, "❌ تحقق من صحة البيانات المدخلة.")

        # ✅ تغيير كلمة المرور
        elif 'change_password' in request.POST:
            pass_form = PasswordChangeForm(request.POST)
            if pass_form.is_valid():
                if user.check_password(pass_form.cleaned_data['old_password']):
                    user.set_password(pass_form.cleaned_data['new_password'])
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, "🔐 تم تغيير كلمة المرور بنجاح.")
                    return redirect('store_settings')
                else:
                    pass_form.add_error('old_password', "❌ كلمة المرور الحالية غير صحيحة.")
            else:
                messages.error(request, "❌ تأكد من تطابق كلمة المرور الجديدة.")

    return render(request, 'stores/store_settings.html', {
        'form': form,
        'pass_form': pass_form
    })

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from orders.models import Order, DeliveryPayment
from datetime import datetime

@login_required
def merchant_payments(request):
    if request.user.user_type != 'merchant':
        return redirect('home')

    # جلب الطلبات المسلمة التي لم يتم دفع مستحقاتها بعد
    orders = Order.objects.filter(
        store__user=request.user,
        status='delivered',
        assigned_to__isnull=False,
        delivery_payment__isnull=True
    ).select_related('assigned_to', 'store')

    if request.method == "POST":
        order_id = request.POST.get("order_id")
        payment_method = request.POST.get("payment_method")
        order = get_object_or_404(Order, id=order_id, store__user=request.user)

        DeliveryPayment.objects.create(
            order=order,
            paid_by=request.user,
            paid_to=order.assigned_to,
            amount=10,
            payment_method=payment_method
        )
        messages.success(request, f"✅ تم دفع مستحقات المندوب {order.assigned_to.get_full_name()} بنجاح.")
        return redirect('merchant_payments')

    return render(request, 'stores/payments.html', {'orders': orders})

from django.db.models import Q, Sum
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User
from orders.models import DeliveryPayment

@login_required
def merchant_payment_history(request):
    if request.user.user_type != 'merchant':
        return redirect('home')

    # استلام قيم الفلترة
    delivery_id = request.GET.get("delivery_id")
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    filters = Q(paid_by=request.user)

    if delivery_id and delivery_id.isdigit():
        filters &= Q(paid_to__id=int(delivery_id))

    if from_date:
        filters &= Q(paid_at__date__gte=from_date)

    if to_date:
        filters &= Q(paid_at__date__lte=to_date)

    payments = DeliveryPayment.objects.filter(filters).select_related('paid_to', 'order', 'order__store')

    total_paid = payments.aggregate(total=Sum('amount'))['total'] or 0

    delivery_users = User.objects.filter(user_type='delivery', is_active=True)

    context = {
        "payments": payments.order_by('-paid_at'),
        "total_paid": total_paid,
        "delivery_users": delivery_users,
        "selected_delivery_id": delivery_id,
        "from_date": from_date,
        "to_date": to_date,
    }

    return render(request, "stores/payment_history.html", context)
