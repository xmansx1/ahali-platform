from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order
from accounts.models import User
from django.http import HttpResponse
import openpyxl
from django.db.models import Q
from .forms import AddUserForm
from stores.models import Store
from django.utils.dateparse import parse_date

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        user = self.request.user

        if user.user_type == 'admin':
            return reverse('admin_dashboard')
        elif user.user_type == 'merchant':
            return reverse('merchant_dashboard')
        elif user.user_type == 'delivery':
            return reverse('delivery_dashboard')
        else:
            messages.error(self.request, "نوع مستخدم غير معروف.")
            return reverse('login')

 
def home_redirect(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    if user.user_type == 'merchant':
        return redirect('merchant_dashboard')
    elif user.user_type == 'delivery':
        return redirect('delivery_dashboard')
    else:
        return redirect('admin:index')  # للمشرفين

from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
import openpyxl

from accounts.models import User
from orders.models import Order


@login_required
def admin_orders(request):
    if request.user.user_type != 'admin':
        return redirect('home')

    selected_merchant_id = request.GET.get('merchant')
    selected_delivery_user_id = request.GET.get('delivery_user')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    export_excel = request.GET.get('export') == 'excel'

    orders = Order.objects.filter(status='delivered').select_related('store', 'assigned_to')

    # فلترة بالتاجر
    if selected_merchant_id and selected_merchant_id.isdigit():
        orders = orders.filter(store__user__id=int(selected_merchant_id))

    # فلترة بالمندوب
    if selected_delivery_user_id and selected_delivery_user_id.isdigit():
        orders = orders.filter(assigned_to__id=int(selected_delivery_user_id))

    # فلترة بالتاريخ
    if date_from:
        try:
            orders = orders.filter(created_at__date__gte=datetime.strptime(date_from, "%Y-%m-%d").date())
        except ValueError:
            messages.error(request, "صيغة التاريخ غير صحيحة (من).")

    if date_to:
        try:
            orders = orders.filter(created_at__date__lte=datetime.strptime(date_to, "%Y-%m-%d").date())
        except ValueError:
            messages.error(request, "صيغة التاريخ غير صحيحة (إلى).")

    if export_excel:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "الطلبات المسلمة"

        headers = ['العميل', 'رقم الجوال', 'الموقع', 'المبلغ', 'المتجر', 'المندوب', 'التاريخ']
        ws.append(headers)

        for order in orders:
            ws.append([
                order.customer_name or '',
                order.customer_phone or '',
                order.customer_location or '',
                order.invoice_amount or '',
                order.store.name if order.store else '',
                order.assigned_to.get_full_name() if order.assigned_to else '',
                order.created_at.strftime('%Y-%m-%d %H:%M'),
            ])

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=delivered_orders.xlsx'
        wb.save(response)
        return response

    merchants = User.objects.filter(user_type='merchant', is_active=True)
    delivery_users = User.objects.filter(user_type='delivery', is_active=True)

    context = {
        'orders': orders.order_by('-created_at'),
        'merchants': merchants,
        'delivery_users': delivery_users,
        'selected_merchant_id': selected_merchant_id,
        'selected_delivery_user_id': selected_delivery_user_id,
        'selected_date_from': date_from,
        'selected_date_to': date_to,
        'order_count': orders.count(),
    }

    return render(request, 'admin/orders.html', context)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def admin_dashboard(request):
    if request.user.user_type != 'admin':
        return redirect('home')

    from accounts.models import User
    from orders.models import Order
    from ads.models import Advertisement  # تأكد أن مسار الاستيراد صحيح حسب مشروعك
    from stores.models import Store

    # الإحصائيات المطلوبة
    total_orders = Order.objects.count()
    delivering_orders = Order.objects.filter(status='delivering').count()
    merchants = User.objects.filter(user_type='merchant').count()
    delivery_users = User.objects.filter(user_type='delivery').count()
    ads_count = Advertisement.objects.count()
    inactive_stores = Store.objects.filter(is_active=False)

    context = {
        'total_orders': total_orders,
        'delivering_orders': delivering_orders,
        'merchants': merchants,
        'delivery_users': delivery_users,
        'ads_count': ads_count,
        'inactive_stores': inactive_stores,
    }

    return render(request, 'admin/dashboard.html', context)

from datetime import datetime
from django.contrib import messages
from orders.models import Order
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def order_archive(request):
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    orders = Order.objects.filter(status='delivered')

    if from_date:
        try:
            from_date_obj = datetime.strptime(from_date, "%Y-%m-%d").date()
            orders = orders.filter(created_at__date__gte=from_date_obj)
        except ValueError:
            messages.error(request, "⚠️ التاريخ (من) غير صالح.")

    if to_date:
        try:
            to_date_obj = datetime.strptime(to_date, "%Y-%m-%d").date()
            orders = orders.filter(created_at__date__lte=to_date_obj)
        except ValueError:
            messages.error(request, "⚠️ التاريخ (إلى) غير صالح.")

    context = {
        "orders": orders.order_by("-created_at"),
        "from_date": from_date,
        "to_date": to_date
    }
    return render(request, "orders/archive.html", context)


from django.shortcuts import get_object_or_404, redirect
from stores.models import Store
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def activate_store(request, store_id):
    if request.user.user_type != 'admin':
        return redirect('home')

    store = get_object_or_404(Store, id=store_id)
    store.is_active = True
    store.save()
    messages.success(request, f"تم تفعيل المتجر: {store.name}")
    return redirect('admin_stores')


@login_required
def admin_users(request):
    if request.user.user_type != 'admin':
        return redirect('home')

    user_type = request.GET.get('type')
    search_query = request.GET.get('q', '')

    users = User.objects.exclude(id=request.user.id)

    if user_type:
        users = users.filter(user_type=user_type)

    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )

    context = {
        'users': users.order_by('-date_joined'),
        'selected_type': user_type,
        'search_query': search_query,
    }
    return render(request, 'admin/users.html', context)

@login_required
def add_user(request):
    if request.user.user_type != 'admin':
        return redirect('home')

    form = AddUserForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        new_user = form.save()
        messages.success(request, "✅ تم إنشاء المستخدم بنجاح")
        return redirect('admin_user_detail', user_id=new_user.id)

    return render(request, 'admin/add_user.html', {'form': form})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.models import User

from orders.models import Order  # تأكد من إضافة هذا الاستيراد في الأعلى

@login_required
def admin_user_detail(request, user_id):
    # ✅ التأكد أن المستخدم الحالي يملك صلاحية المشرف
    if request.user.user_type != 'admin':
        messages.error(request, "غير مصرح لك بالوصول لهذه الصفحة.")
        return redirect('home')

    # ✅ الحصول على المستخدم المطلوب أو عرض 404
    target_user = get_object_or_404(User, id=user_id)

    # ✅ محاولة الحصول على المتجر المرتبط بالمستخدم، إن وجد
    store = getattr(target_user, 'store', None)

    # ✅ احتساب عدد الطلبات المسلمة إذا كان المستخدم مندوب
    delivered_orders_count = 0
    if target_user.user_type == 'delivery':
        delivered_orders_count = Order.objects.filter(
            assigned_to=target_user,
            status='delivered'
        ).count()

    # ✅ تجهيز البيانات لإرسالها إلى القالب
    context = {
        'target_user': target_user,
        'store': store,
        'delivered_orders_count': delivered_orders_count,  # ✅ تمرير العدد للقالب
    }

    return render(request, 'admin/user_detail.html', context)


@login_required
def admin_store_detail(request, user_id):
    if request.user.user_type != 'admin':
        return redirect('home')

    merchant = get_object_or_404(User, id=user_id, user_type='merchant')

    return render(request, 'admin/admin_store_detail.html', {'user': merchant})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from accounts.models import User
from .forms import EditUserForm, PasswordChangeAdminForm

@login_required
def edit_user(request, user_id):
    if request.user.user_type != 'admin':
        return redirect('home')

    user = get_object_or_404(User, id=user_id)
    form = EditUserForm(request.POST or None, instance=user)
    pass_form = PasswordChangeAdminForm(request.POST or None)

    if 'save_user' in request.POST and form.is_valid():
        form.save()
        messages.success(request, "✅ تم تحديث بيانات المستخدم.")
        return redirect('admin_user_detail', user_id=user.id)

    if 'change_password' in request.POST and pass_form.is_valid():
        new_pass = pass_form.cleaned_data['new_password']
        user.set_password(new_pass)
        user.save()
        messages.success(request, "🔐 تم تغيير كلمة المرور بنجاح.")
        return redirect('admin_user_detail', user_id=user.id)

    context = {
        'form': form,
        'pass_form': pass_form,
        'user_obj': user,
    }
    return render(request, 'admin/edit_user.html', context)

# accounts/views.py أو core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import User
from accounts.forms import EditStoreForm

@login_required
def admin_store_edit(request, user_id):
    if request.user.user_type != 'admin':
        return redirect('home')

    merchant = get_object_or_404(User, id=user_id, user_type='merchant')
    form = EditStoreForm(request.POST or None, instance=merchant)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('admin_store_detail', user_id=merchant.id)

    return render(request, 'admin/store_edit.html', {'form': form, 'merchant': merchant})

from accounts.forms import AdminPasswordChangeForm


@login_required
def admin_change_password(request, user_id):
    if request.user.user_type != 'admin':
        return redirect('home')

    user = get_object_or_404(User, id=user_id)

    form = AdminPasswordChangeForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        new_password = form.cleaned_data['new_password']
        user.set_password(new_password)
        user.save()
        messages.success(request, f"تم تغيير كلمة المرور للمستخدم {user.username} بنجاح.")
        return redirect('admin_user_detail', user_id=user.id)

    return render(request, 'admin/change_password.html', {'form': form, 'target_user': user})

from accounts.forms import UserEditForm


@login_required
def admin_edit_user(request, user_id):
    if request.user.user_type != 'admin':
        messages.warning(request, "🚫 ليس لديك صلاحية الوصول لهذه الصفحة.")
        return redirect('home')

    user = get_object_or_404(User, id=user_id)

    # 🟢 تعريف النماذج
    form = UserEditForm(request.POST or None, instance=user)
    pass_form = PasswordChangeAdminForm(request.POST or None)

    # 🧠 تعديل بيانات المستخدم
    if request.method == 'POST':
        if 'save_user' in request.POST and form.is_valid():
            form.save()
            messages.success(request, "✅ تم حفظ بيانات المستخدم بنجاح.")
            return redirect('admin_edit_user', user_id=user.id)

        elif 'change_password' in request.POST and pass_form.is_valid():
            new_password = pass_form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            messages.success(request, "🔐 تم تغيير كلمة المرور بنجاح.")
            return redirect('admin_edit_user', user_id=user.id)

    context = {
        'form': form,
        'pass_form': pass_form,
        'user_obj': user,
    }
    return render(request, 'admin/admin_user_edit.html', context)

@login_required
def merchant_orders(request):
    # لاحقًا تضيف الفلاتر للطلبات الخاصة بالتاجر فقط
    return render(request, 'merchant/orders.html')



def admin_stores_view(request):
    query = request.GET.get('q', '')
    stores = Store.objects.select_related('user').all()

    if query:
        stores = stores.filter(
            Q(user__username__icontains=query) |
            Q(name__icontains=query) |
            Q(address__icontains=query)
        )

    context = {
        'stores': stores,
        'search_query': query,
    }
    return render(request, 'admin/stores.html', context)

from django.shortcuts import render, get_object_or_404
from stores.models import Store

def admin_store_detail_view(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    return render(request, 'admin/admin_store_detail.html', {'store': store})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from stores.models import Store
from stores.forms import StoreForm  # تأكد أن هذا هو النموذج الصحيح

@login_required
def admin_store_edit_view(request, store_id):
    if request.user.user_type != 'admin':
        messages.error(request, "🚫 غير مصرح لك بالوصول إلى هذه الصفحة.")
        return redirect('home')

    store = get_object_or_404(Store, id=store_id)

    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            store_instance = form.save(commit=False)
            store_instance.is_active = store.is_active  # ✅ نحافظ على حالة التفعيل كما هي
            store_instance.save()
            messages.success(request, "✅ تم تحديث بيانات المتجر بنجاح.")
            return redirect('admin_store_detail', store_id=store.id)
        else:
            messages.error(request, "❌ حدث خطأ أثناء حفظ البيانات. تأكد من صحة الحقول.")
    else:
        form = StoreForm(instance=store)

    return render(request, 'admin/store_edit.html', {
        'form': form,
        'store': store,
    })

from django.contrib.auth import get_user_model

@login_required
def delete_user(request, user_id):
    if request.user.user_type != 'admin':
        messages.error(request, "🚫 لا تملك صلاحية حذف المستخدمين.")
        return redirect('admin_users')

    user = get_object_or_404(get_user_model(), id=user_id)

    if request.method == 'POST':
        user.delete()
        messages.success(request, "✅ تم حذف المستخدم بنجاح.")
        return redirect('admin_users')

    messages.error(request, "❌ لا يمكن تنفيذ الحذف إلا عبر POST.")
    return redirect('admin_users')

# accounts/views.py
from orders.models import Order  # تأكد من وجود هذا الاستيراد

@login_required
def delivery_detail(request, user_id):
    if request.user.user_type != 'admin':
        messages.error(request, "🚫 غير مصرح لك.")
        return redirect('admin_users')

    user = get_object_or_404(get_user_model(), id=user_id, user_type='delivery')

    # ✅ حساب عدد الطلبات المسلمة للمندوب
    delivered_orders_count = Order.objects.filter(
        assigned_to=user,
        status='delivered'
    ).count()

    return render(request, 'admin/delivery_detail.html', {
        'delivery': user,
        'delivered_orders_count': delivered_orders_count,  # ✅ تمرير العدد للقالب
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.models import User
from orders.models import Order  # تأكد من وجود هذا المسار الصحيح حسب مشروعك

@login_required
def admin_edit_delivery_view(request, delivery_id):
    if request.user.user_type != 'admin':
        messages.error(request, "🚫 غير مصرح لك بالوصول إلى هذه الصفحة.")
        return redirect('home')

    delivery = get_object_or_404(User, id=delivery_id, user_type='delivery')
    total_delivered_orders = Order.objects.filter(assigned_to=delivery, status='delivered').count()


    if request.method == 'POST':
        username = request.POST.get('username')
        phone = request.POST.get('phone_number')
        email = request.POST.get('email')
        password = request.POST.get('password')

        delivery.username = username
        delivery.phone_number = phone
        delivery.email = email

        if password:
            delivery.set_password(password)

        delivery.save()
        messages.success(request, "✅ تم تحديث بيانات المندوب بنجاح.")
        return redirect('admin_edit_delivery', delivery_id=delivery.id)

    return render(request, 'admin/delivery_edit.html', {
        'delivery': delivery,
        'total_delivered_orders': total_delivered_orders
    })

    
@login_required
def toggle_user_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()

    action = "تم تفعيل" if user.is_active else "تم تعطيل"
    messages.success(request, f"✅ {action} المستخدم: {user.get_full_name() or user.username}")
    return redirect('admin_users')

@login_required
def toggle_store_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if hasattr(user, 'store'):
        store = user.store
        store.is_active = not store.is_active
        store.save()
        if store.is_active:
            messages.success(request, f"✅ تم تنشيط المتجر: {store.name}")
        else:
            messages.warning(request, f"❌ تم تعطيل المتجر: {store.name}")
    else:
        messages.error(request, "❌ هذا المستخدم لا يملك متجرًا")
    return redirect('admin_users')