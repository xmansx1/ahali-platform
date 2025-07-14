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