from django.urls import path
from django.http import HttpResponse
from django.contrib.auth.views import LoginView, LogoutView
from . import views  # ✅ الاستيراد الصحيح

urlpatterns = [

    # ✅ تسجيل الدخول والخروج
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

    # ✅ إعادة توجيه حسب نوع المستخدم
    path('', views.home_redirect, name='home'),

    # ✅ لوحة المشرف
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/orders/', views.admin_orders, name='admin_orders'),

    # ✅ إدارة المستخدمين
    path('admin/users/', views.admin_users, name='admin_users'),
    path('admin/users/add/', views.add_user, name='add_user'),
    path('admin/users/<int:user_id>/', views.admin_user_detail, name='admin_user_detail'),
    path('admin/users/<int:user_id>/edit/', views.admin_edit_user, name='admin_edit_user'),
    path('admin/users/<int:user_id>/change-password/', views.admin_change_password, name='admin_change_password'),
    path('admin/users/toggle/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    path('admin/users/<int:user_id>/toggle-store/', views.toggle_store_status, name='toggle_store_status'),  # ✅ هنا تم تصحيحها

    # ✅ لوحة التاجر
    path('merchant/orders/', views.merchant_orders, name='merchant_orders'),

    # ✅ إدارة المتاجر
    path('admin/stores/', views.admin_stores_view, name='admin_stores'),
    path('admin/stores/<int:store_id>/', views.admin_store_detail_view, name='admin_store_detail'),
    path('admin/stores/<int:store_id>/edit/', views.admin_store_edit_view, name='admin_store_edit'),
    path('admin/stores/<int:store_id>/activate/', views.activate_store, name='activate_store'),

    # ✅ صفحة اختبار مؤقتة
    path('test/', lambda request: HttpResponse("صفحة حسابات الاختبار")),
    
 ]
