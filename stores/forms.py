from django import forms
from stores.models import Store


class StoreSettingsForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['phone', 'is_available', 'address', 'latitude', 'longitude']
        labels = {
            'phone': 'رقم الجوال',
            'address': 'عنوان المتجر',
            'is_available': 'متاح لاستقبال الطلبات',
        }
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'w-full border rounded px-3 py-2',
                'placeholder': 'مثال: 0551234567'
            }),
            'address': forms.TextInput(attrs={
                'class': 'w-full border rounded px-3 py-2',
                'placeholder': 'مثال: حي الربيع، الرياض'
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-green-600 border-gray-300 rounded'
            }),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }

    def clean_is_available(self):
        value = self.data.get('is_available')
        return value == 'on'  # ✅ يُعيد True فقط إذا كانت القيمة 'on'


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
