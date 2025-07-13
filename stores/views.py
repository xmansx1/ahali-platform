from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import StoreSettingsForm, PasswordChangeForm
from stores.models import Store

@login_required
def store_settings(request):
    user = request.user

    if user.user_type != 'merchant':
        messages.error(request, "غير مصرح لك بالوصول لهذه الصفحة.")
        return redirect('home')

    try:
        store = user.store
    except Store.DoesNotExist:
        messages.error(request, "لم يتم ربط المستخدم بمتجر.")
        return redirect('home')

    form = StoreSettingsForm(instance=store)
    pass_form = PasswordChangeForm()

    if request.method == 'POST':
        # ✅ حفظ إعدادات المتجر
        if 'save_settings' in request.POST:
            print("✅ POST DATA:", request.POST.dict())  # للتحقق من is_available
            form = StoreSettingsForm(request.POST, instance=store)
            if form.is_valid():
                form.save()
                messages.success(request, "✅ تم تحديث بيانات المتجر بنجاح.")
                return redirect('store_settings')
            else:
                messages.error(request, "❌ تحقق من صحة البيانات المدخلة.")

        # ✅ تغيير كلمة المرور
        elif 'change_password' in request.POST:
            pass_form = PasswordChangeForm(request.POST)
            if pass_form.is_valid():
                if user.check_password(pass_form.cleaned_data['old_password']):
                    user.set_password(pass_form.cleaned_data['new_password'])
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, "🔐 تم تغيير كلمة المرور بنجاح.")
                    return redirect('store_settings')
                else:
                    pass_form.add_error('old_password', "❌ كلمة المرور الحالية غير صحيحة.")
            else:
                messages.error(request, "❌ تأكد من تطابق كلمة المرور الجديدة.")

    return render(request, 'stores/store_settings.html', {
        'form': form,
        'pass_form': pass_form
    })
