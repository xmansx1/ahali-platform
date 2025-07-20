from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Advertisement
from .forms import AdvertisementForm

def admin_ads_list(request):
    ads = Advertisement.objects.all()
    return render(request, 'ads/ad_list.html', {'ads': ads})

def ad_create(request):
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "تمت إضافة الإعلان بنجاح.")
            return redirect('ads:admin_ads_list')
    else:
        form = AdvertisementForm()
    return render(request, 'ads/ad_ads.html', {'form': form})

def ad_edit(request, ad_id):
    ad = get_object_or_404(Advertisement, id=ad_id)
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تعديل الإعلان بنجاح.")
            return redirect('ads:admin_ads_list')
    else:
        form = AdvertisementForm(instance=ad)
    return render(request, 'ads/ads_edit.html', {'form': form, 'ad': ad})

def ad_delete(request, ad_id):
    ad = get_object_or_404(Advertisement, id=ad_id)
    if request.method == 'POST':
        ad.delete()
        messages.success(request, "تم حذف الإعلان.")
        return redirect('ads:admin_ads_list')
    return redirect('ads:admin_ads_list')

# ads/views.py
from django.shortcuts import render, get_object_or_404
from .models import Advertisement

def ad_detail(request, ad_id):
    ad = get_object_or_404(Advertisement, pk=ad_id, is_active=True)
    return render(request, 'ads/ad_detail.html', {'ad': ad})

from ads.models import WelcomePopup

def home(request):
    popup = WelcomePopup.objects.filter(is_active=True).order_by('-created_at').first()
    return render(request, 'core/home.html', {'popup': popup})

from django.shortcuts import render, redirect, get_object_or_404
from .models import WelcomePopup
from .forms import WelcomePopupForm
from django.contrib import messages

# 📋 عرض قائمة النوافذ
def popup_list(request):
    popups = WelcomePopup.objects.all()
    return render(request, 'ads/popup_list.html', {'popups': popups})

# ➕ إنشاء نافذة جديدة
def popup_create(request):
    if request.method == 'POST':
        form = WelcomePopupForm(request.POST, request.FILES)  # ✅ تم التعديل هنا
        if form.is_valid():
            form.save()
            messages.success(request, "تم إضافة النافذة الترحيبية بنجاح.")
            return redirect('ads:popup_list')
    else:
        form = WelcomePopupForm()
    return render(request, 'ads/popup_form.html', {'form': form, 'title': 'إضافة نافذة ترحيبية'})

# ✏️ تعديل نافذة
def popup_edit(request, popup_id):
    popup = get_object_or_404(WelcomePopup, pk=popup_id)
    if request.method == 'POST':
        form = WelcomePopupForm(request.POST, request.FILES, instance=popup)  # ✅ تم التعديل هنا
        if form.is_valid():
            form.save()
            messages.success(request, "تم تعديل النافذة بنجاح.")
            return redirect('ads:popup_list')
    else:
        form = WelcomePopupForm(instance=popup)
    return render(request, 'ads/popup_form.html', {'form': form, 'title': 'تعديل النافذة الترحيبية'})

# ❌ حذف نافذة
def popup_delete(request, pk):
    popup = get_object_or_404(WelcomePopup, pk=pk)
    popup.delete()
    messages.success(request, "تم حذف النافذة.")
    return redirect('ads:popup_list')

# 🔄 تفعيل/تعطيل
def popup_toggle(request, pk):
    popup = get_object_or_404(WelcomePopup, pk=pk)
    popup.is_active = not popup.is_active
    popup.save()
    messages.success(request, f"تم {'تفعيل' if popup.is_active else 'تعطيل'} النافذة.")
    return redirect('ads:popup_list')
