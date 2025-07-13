from core.views import home
from django.urls import path
from .views import public_store_browser

urlpatterns = [
    path('', home, name='home'),
    path('stores/', public_store_browser, name='public_store_browser'),
]
