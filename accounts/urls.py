from django.urls import path
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from . import views
from django.contrib.auth.views import LogoutView

from accounts.views import (
    admin_change_password,
    admin_edit_user,
    admin_store_edit,
)

# ✅ اختبار
def test_view(request):
    return HttpResponse("صفحة حسابات الاختبار")

urlpatterns = [

    # ✅ تسجيل الدخول
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),

    # ✅ إعادة توجيه حسب نوع المستخدم
    path('', views.home_redirect, name='home'),

    # ✅ لوحة المشرف
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/orders/', views.admin_orders, name='admin_orders'),
    path('admin/users/<int:user_id>/', views.admin_user_detail, name='admin_user_detail'),

    # ✅ إدارة المستخدمين
    path('admin/users/', views.admin_users, name='admin_users'),
    path('admin/users/add/', views.add_user, name='add_user'),
    path('admin/users/toggle/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    path('admin/users/<int:user_id>/edit/', admin_edit_user, name='admin_edit_user'),
    path('admin/users/<int:user_id>/change-password/', admin_change_password, name='admin_change_password'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('merchant/orders/', views.merchant_orders, name='merchant_orders'),
    path('accounts/logout/', LogoutView.as_view(next_page='/'), name='logout'),

    # ✅ إدارة المتاجر
    path('admin/stores/', views.admin_stores, name='admin_stores'),
    path('admin/stores/<int:user_id>/edit/', admin_store_edit, name='admin_store_edit'),
]
