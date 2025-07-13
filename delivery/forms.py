from django import forms
from accounts.models import User

class DeliverySettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone_number']
        labels = {
            'phone_number': 'رقم الجوال',
        }
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
