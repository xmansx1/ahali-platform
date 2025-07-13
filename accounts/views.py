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

@login_required
def admin_dashboard(request):
    if request.user.user_type != 'admin':
        return redirect('home')

    total_orders = Order.objects.count()
    delivering_orders = Order.objects.filter(status='delivering').count()
    merchants = User.objects.filter(user_type='merchant').count()
    delivery_users = User.objects.filter(user_type='delivery').count()

    context = {
        'total_orders': total_orders,
        'delivering_orders': delivering_orders,
        'merchants': merchants,
        'delivery_users': delivery_users,
    }
    return render(request, 'admin/dashboard.html', context)

@login_required
def admin_orders(request):
    if request.user.user_type != 'admin':
        return redirect('home')

    selected_merchant_id = request.GET.get('merchant')
    selected_date = request.GET.get('date')
    export_excel = request.GET.get('export') == 'excel'

    orders = Order.objects.filter(status='delivered')

    if selected_merchant_id:
        orders = orders.filter(store_id=selected_merchant_id)
    if selected_date:
        orders = orders.filter(created_at__date=selected_date)

    if export_excel:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "الطلبات المسلمة"

        headers = ['العميل', 'رقم الجوال', 'الموقع', 'المبلغ', 'المتجر', 'المندوب', 'التاريخ']
        ws.append(headers)

        for order in orders:
            ws.append([
                order.customer_name,
                order.customer_phone,
                order.customer_location,
                order.invoice_amount or '',
                order.store.name,
                order.assigned_to.username if order.assigned_to else '',
                order.created_at.strftime('%Y-%m-%d %H:%M'),
            ])

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=delivered_orders.xlsx'
        wb.save(response)
        return response

    merchants = User.objects.filter(user_type='merchant')
    order_count = orders.count()

    context = {
        'orders': orders.order_by('-created_at'),
        'merchants': merchants,
        'selected_merchant_id': selected_merchant_id,
        'selected_date': selected_date,
        'order_count': order_count,
    }
    return render(request, 'admin/orders.html', context)


@login_required
def toggle_user_status(request, user_id):
    if request.user.user_type != 'admin':
        return redirect('home')

    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    messages.success(request, f"تم تحديث حالة المستخدم: {user.username}")
    return redirect('admin_users')

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


@login_required
def admin_user_detail(request, user_id):
    if request.user.user_type != 'admin':
        return redirect('home')

    user = get_object_or_404(User, id=user_id)

    return render(request, 'admin/users/detail.html', {'user_obj': user})

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
        return redirect('home')

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ تم تعديل بيانات المستخدم بنجاح.")
            return redirect('admin_users')
    else:
        form = UserEditForm(instance=user)

    return render(request, 'admin/admin_user_edit.html', {'form': form, 'user_obj': user})

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
    return render(request, 'admin/user_detail.html', {'store': store})


from stores.forms import StoreForm  # تأكد أن لديك هذا النموذج

def admin_store_edit_view(request, store_id):
    store = get_object_or_404(Store, id=store_id)

    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            form.save()
            return redirect('admin_stores')
    else:
        form = StoreForm(instance=store)

    return render(request, 'admin/store_edit.html', {
        'form': form,
        'store': store
    })