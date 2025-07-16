from django.urls import path
from .views import store_settings
from . import views

urlpatterns = [
    path('settings/', store_settings, name='store_settings'),
    path('payments/', views.merchant_payments, name='merchant_payments'),
    path('payments/history/', views.merchant_payment_history, name='merchant_payment_history'),

]
