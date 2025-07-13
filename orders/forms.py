from django import forms
from .models import StoreOrder
import re
from django.core.exceptions import ValidationError

class StoreOrderForm(forms.ModelForm):

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not re.match(r'^05\d{8}$', phone):
            raise ValidationError('يرجى إدخال رقم جوال سعودي صحيح يبدأ بـ 05 ويتكون من 10 أرقام.')
        return phone

    class Meta:
        model = StoreOrder
        fields = ['full_name', 'phone_number', 'order_details', 'order_type', 'location_lat', 'location_lng']
        labels = {
            'full_name': 'الاسم الكامل',
            'phone_number': 'رقم الجوال',
            'order_details': 'تفاصيل الطلب',
            'order_type': 'نوع الطلب',
            'location_lat': 'خط العرض',
            'location_lng': 'خط الطول',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'أدخل الاسم الكامل'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': '05XXXXXXXX'
            }),
            'order_details': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'مثلاً: أحتاج 3 عبوات مياه وعلبة خبز...',
                'rows': 3
            }),
            'order_type': forms.RadioSelect(choices=[
                ('pickup', 'استلام من المحل'),
                ('delivery', 'توصيل')
            ]),
            'location_lat': forms.HiddenInput(),
            'location_lng': forms.HiddenInput(),
        }
