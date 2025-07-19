from django import forms
from stores.models import Store
from django import forms
from stores.models import Store

class StoreSettingsForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = [
            'phone', 'address', 'latitude', 'longitude',
            'is_available', 'delivery_fee', 'customer_delivery_share',
            'delivery_policy_note'  # ✅ الحقل الجديد
        ]
        labels = {
            'phone': '📞 رقم الجوال',
            'address': '📍 عنوان المتجر',
            'latitude': '📍 خط العرض',
            'longitude': '📍 خط الطول',
            'is_available': '📦 المتجر متاح لاستقبال الطلبات',
            'delivery_fee': '🚚 مبلغ التوصيل (ريال)',
            'customer_delivery_share': '🧮 النسبة التي يتحملها العميل من التوصيل (%)',
            'delivery_policy_note': '📢 سياسة التوصيل (اختياري)',
        }
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'w-full border rounded px-3 py-2',
                'placeholder': 'مثال: 0551234567',
                'dir': 'ltr'
            }),
            'address': forms.TextInput(attrs={
                'class': 'w-full border rounded px-3 py-2',
                'placeholder': 'مثال: حي الربيع، الرياض'
            }),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-green-600 border-gray-300 rounded'
            }),
            'delivery_fee': forms.NumberInput(attrs={
                'class': 'w-full border rounded px-3 py-2',
                'placeholder': 'مثال: 10.00',
                'step': '0.50',
                'min': '0'
            }),
            'customer_delivery_share': forms.NumberInput(attrs={
                'class': 'w-full border rounded px-3 py-2',
                'placeholder': 'مثال: 40 (يعني 40% يتحملها العميل)',
                'step': '1',
                'min': '0',
                'max': '100'
            }),
            'delivery_policy_note': forms.Textarea(attrs={
                'class': 'w-full border rounded px-3 py-2',
                'placeholder': 'مثال: 🚚 التوصيل مجاني للطلبات فوق 50 ريال',
                'rows': 3
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.data:
            self.data = self.data.copy()
            self.data['is_available'] = self.data.get('is_available') == 'on'

    def clean_delivery_fee(self):
        value = self.cleaned_data.get('delivery_fee')
        if value is not None and value < 10:
            raise forms.ValidationError("🚫 الحد الأدنى لمبلغ التوصيل هو 10 ريال.")
        return value

    def clean_customer_delivery_share(self):
        value = self.cleaned_data.get('customer_delivery_share')
        if value is not None and not (0 <= value <= 100):
            raise forms.ValidationError("⚠️ النسبة يجب أن تكون بين 0 و 100.")
        return value


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full border rounded px-3 py-2',
            'placeholder': 'أدخل كلمة المرور الحالية'
        }),
        label='كلمة المرور الحالية'
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full border rounded px-3 py-2',
            'placeholder': 'أدخل كلمة المرور الجديدة'
        }),
        label='كلمة المرور الجديدة'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full border rounded px-3 py-2',
            'placeholder': 'أعد كتابة كلمة المرور'
        }),
        label='تأكيد كلمة المرور'
    )

    def clean(self):
        cleaned_data = super().clean()
        new = cleaned_data.get('new_password')
        confirm = cleaned_data.get('confirm_password')
        if new and confirm and new != confirm:
            raise forms.ValidationError("كلمة المرور الجديدة غير متطابقة.")
        return cleaned_data

from django import forms
from .models import Store


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = [
            'name', 'phone', 'address',
            'latitude', 'longitude', 'store_type',
            'is_available'  # ✅ نزيل is_active من هنا لحمايته من الإلغاء التلقائي
        ]
        labels = {
            'name': 'اسم المتجر',
            'phone': 'رقم الجوال',
            'address': 'العنوان',
            'latitude': 'خط العرض',
            'longitude': 'خط الطول',
            'store_type': 'نوع المتجر',
            'is_available': 'متاح لاستقبال الطلبات؟',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'address': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'latitude': forms.NumberInput(attrs={'step': 'any', 'class': 'form-input'}),
            'longitude': forms.NumberInput(attrs={'step': 'any', 'class': 'form-input'}),
            'store_type': forms.Select(attrs={'class': 'form-select'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
