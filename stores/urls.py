from django.urls import path
from .views import store_settings

urlpatterns = [
    path('settings/', store_settings, name='store_settings'),
]
