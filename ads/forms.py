from django import forms
from .models import Advertisement

class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title', 'text', 'link', 'image', 'is_active']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2',
                'placeholder': 'مثال: عروض حصرية على المنتجات 🛍️',
                'rows': 4,
            }),
        }


from django import forms
from .models import WelcomePopup

class WelcomePopupForm(forms.ModelForm):
    class Meta:
        model = WelcomePopup
        fields = ['title', 'message', 'image', 'is_active']
        labels = {
            'title': 'عنوان النافذة',
            'message': 'نص الرسالة',
            'image': 'صورة ترحيبية (اختياري)',
            'is_active': 'مفعلة؟',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full border px-4 py-2 rounded',
                'placeholder': 'مثال: مرحبًا بكم في المنصة'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full border px-4 py-2 rounded h-32',
                'placeholder': 'نص الرسالة الترحيبية'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full border px-2 py-1 rounded'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-5 w-5 text-blue-600'
            }),
        }
