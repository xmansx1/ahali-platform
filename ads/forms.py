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
