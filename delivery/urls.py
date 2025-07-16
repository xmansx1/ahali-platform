from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.delivery_dashboard, name='delivery_dashboard'),
    path('accept/<int:order_id>/', views.accept_order, name='accept_order'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('complete/<int:order_id>/', views.complete_order, name='complete_order'),
    path('archive/', views.delivery_archive, name='delivery_archive'),
    path('settings/', views.delivery_settings, name='delivery_settings'),
    path('delivery/earnings/', views.delivery_earnings, name='delivery_earnings'),

 ]
