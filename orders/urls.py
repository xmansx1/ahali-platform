from django.urls import path
from . import views

urlpatterns = [
    # لوحة التاجر
    path('merchant/dashboard/', views.merchant_dashboard, name='merchant_dashboard'),
    path('archive/', views.merchant_archive, name='merchant_archive'),

    # طلبات التاجر
    path('order/<int:order_id>/update/', views.update_order_status, name='update_order_status'),
    path('merchant/orders/partial/', views.merchant_orders_partial, name='merchant_orders_partial'),

    # العدادات
    path('merchant/status_counts/', views.merchant_status_counts, name='merchant_status_counts'),
    path('dashboard/counters/', views.merchant_counters_partial, name='merchant_counters_partial'),
    path('admin/status_counts/', views.admin_order_status_counts, name='admin_order_status_counts'),

    # تفاصيل الطلب
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('<int:order_id>/detail/', views.order_detail_ajax, name='order_detail_ajax'),

    # استقبال الطلب من الزائر
    path('submit-order/<int:store_id>/', views.submit_store_order, name='submit_store_order'),
    path('orders/merchant/orders-partial/', views.merchant_orders_partial, name='merchant_orders_partial'),

]
