from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from stores.models import Store
from orders.models import Order  # تأكد أن هذا النموذج يحتوي الحقول اللازمة
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect


from django.db.models import Q
def public_store_browser(request):
    query = request.GET.get("q", "")
    stores = Store.objects.filter(is_active=True, is_available=True)

    if query:
        stores = stores.filter(name__icontains=query) | stores.filter(address__icontains=query)

    context = {
        "stores": stores,
    }
    return render(request, "public/store_browser.html", context)
