from django.urls import path
from . import views

app_name = "ads"

urlpatterns = [
    path('admin/', views.admin_ads_list, name='admin_ads_list'),
    path('admin/create/', views.ad_create, name='ad_create'),
    path('admin/<int:ad_id>/edit/', views.ad_edit, name='ad_edit'),
    path('admin/<int:ad_id>/delete/', views.ad_delete, name='ad_delete'),
    path('<int:ad_id>/', views.ad_detail, name='ad_detail'),
    path('<int:ad_id>/', views.ad_detail, name='detail'),
    path('welcome-popups/', views.popup_list, name='popup_list'),
    path('welcome-popups/create/', views.popup_create, name='popup_create'),
    path('welcome-popups/<int:popup_id>/edit/', views.popup_edit, name='popup_edit'),
    path('welcome-popups/<int:popup_id>/delete/', views.popup_delete, name='popup_delete'),
]