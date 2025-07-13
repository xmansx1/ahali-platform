from django.urls import path
from django.http import HttpResponse
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    home_redirect, admin_dashboard, admin_orders, admin_user_detail,
    admin_users, add_user, toggle_user_status, merchant_orders,
    admin_store_detail_view, admin_store_edit_view, admin_stores_view,
    admin_change_password, admin_edit_user
)

# ✅ اختبار
def test_view(request):
    return HttpResponse("صفحة حسابات الاختبار")

urlpatterns = [

    # ✅ تسجيل الدخول والخروج
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page='/'), name='logout'),

    # ✅ إعادة توجيه حسب نوع المستخدم
    path('', home_redirect, name='home'),

    # ✅ لوحة المشرف
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/orders/', admin_orders, name='admin_orders'),

    # ✅ إدارة المستخدمين
    path('admin/users/', admin_users, name='admin_users'),
    path('admin/users/add/', add_user, name='add_user'),
    path('admin/users/<int:user_id>/', admin_user_detail, name='admin_user_detail'),
    path('admin/users/<int:user_id>/edit/', admin_edit_user, name='admin_edit_user'),
    path('admin/users/<int:user_id>/change-password/', admin_change_password, name='admin_change_password'),
    path('admin/users/toggle/<int:user_id>/', toggle_user_status, name='toggle_user_status'),

    # ✅ لوحة التاجر
    path('merchant/orders/', merchant_orders, name='merchant_orders'),

    # ✅ إدارة المتاجر
    path('admin/stores/', admin_stores_view, name='admin_stores'),
    path('admin/stores/<int:store_id>/', admin_store_detail_view, name='admin_store_detail'),
    path('admin/stores/<int:store_id>/edit/', admin_store_edit_view, name='admin_store_edit'),

    # ✅ اختبار
    path('test/', test_view),
]
