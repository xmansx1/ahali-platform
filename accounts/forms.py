from django import forms
from accounts.models import User

class AddUserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "input", "placeholder": "أدخل كلمة المرور"}),
        label="كلمة المرور"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "input", "placeholder": "أعد إدخال كلمة المرور"}),
        label="تأكيد كلمة المرور"
    )

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email',       # ✅ مضافة حديثًا
            'phone_number', 'user_type', 'is_active',
            'store_location', 'store_latitude', 'store_longitude'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input', 'placeholder': 'اسم المستخدم'}),
            'first_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'الاسم الأول'}),
            'last_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'اسم العائلة'}),
            'email': forms.EmailInput(attrs={'class': 'input', 'placeholder': 'example@email.com'}),
            'phone_number': forms.TextInput(attrs={'class': 'input', 'placeholder': '05xxxxxxxx'}),
            'user_type': forms.Select(attrs={'class': 'input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'checkbox'}),
            'store_location': forms.TextInput(attrs={'class': 'input', 'placeholder': 'مثال: حي الياسمين'}),
            'store_latitude': forms.HiddenInput(),
            'store_longitude': forms.HiddenInput(),
        }
        labels = {
            'username': 'اسم المستخدم',
            'first_name': 'الاسم الأول',
            'last_name': 'اسم العائلة',
            'email': 'البريد الإلكتروني',
            'phone_number': 'رقم الجوال',
            'user_type': 'نوع المستخدم',
            'is_active': 'تفعيل الحساب',
            'store_location': 'عنوان المتجر',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")
        user_type = cleaned_data.get("user_type")

        # ✅ تأكد من تطابق كلمتي المرور
        if password and confirm and password != confirm:
            raise forms.ValidationError("كلمتا المرور غير متطابقتين.")

        # ✅ التحقق من بيانات المتجر إذا كان المستخدم تاجر
        if user_type == 'merchant':
            if not cleaned_data.get('store_location'):
                raise forms.ValidationError("يرجى تحديد عنوان المتجر.")
            if not cleaned_data.get('store_latitude') or not cleaned_data.get('store_longitude'):
                raise forms.ValidationError("يرجى تحديد موقع المتجر على الخريطة.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        # ❌ امسح بيانات الموقع إن لم يكن تاجر
        if user.user_type != 'merchant':
            user.store_location = None
            user.store_latitude = None
            user.store_longitude = None

        if commit:
            user.save()
        return user

from django import forms
from accounts.models import User

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'phone_number', 'user_type', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input'}),
            'phone_number': forms.TextInput(attrs={'class': 'input'}),
            'user_type': forms.Select(attrs={'class': 'input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'checkbox'}),
        }

class PasswordChangeAdminForm(forms.Form):
    new_password = forms.CharField(
        label="كلمة مرور جديدة",
        widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': '••••••••'})
    )

from accounts.models import User

class EditStoreForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'phone_number', 'store_location', 'store_latitude', 'store_longitude', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input', 'placeholder': 'اسم المستخدم'}),
            'phone_number': forms.TextInput(attrs={'class': 'input', 'placeholder': '05xxxxxxxx'}),
            'store_location': forms.TextInput(attrs={'class': 'input', 'placeholder': 'مثال: حي الياسمين'}),
            'store_latitude': forms.HiddenInput(),
            'store_longitude': forms.HiddenInput(),
            'is_active': forms.CheckboxInput(attrs={'class': 'checkbox'}),
        }
        labels = {
            'username': 'اسم التاجر',
            'phone_number': 'رقم الجوال',
            'store_location': 'عنوان المتجر',
            'is_active': 'تفعيل الحساب',
        }

from django import forms

class AdminPasswordChangeForm(forms.Form):
    new_password = forms.CharField(
        label="كلمة المرور الجديدة",
        widget=forms.PasswordInput(attrs={"class": "input", "placeholder": "••••••••"})
    )
    confirm_password = forms.CharField(
        label="تأكيد كلمة المرور",
        widget=forms.PasswordInput(attrs={"class": "input", "placeholder": "••••••••"})
    )

    def clean(self):
        cleaned_data = super().clean()
        new_pass = cleaned_data.get("new_password")
        confirm = cleaned_data.get("confirm_password")

        if new_pass and confirm and new_pass != confirm:
            raise forms.ValidationError("كلمتا المرور غير متطابقتين.")
        return cleaned_data

from accounts.models import User


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'phone_number',
            'user_type',           # ✅ إضافة نوع المستخدم
            'store_location',
            'store_latitude',
            'store_longitude',
            'is_active',
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'اسم المستخدم'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'مثال: 0551234567'
            }),
            'user_type': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500',
            }),
            'store_location': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'الحي، المدينة'
            }),
            'store_latitude': forms.HiddenInput(),
            'store_longitude': forms.HiddenInput(),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-checkbox text-blue-600 rounded',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        # ✅ تحسين النصوص الظاهرة للعربية
        self.fields['username'].label = "اسم المستخدم"
        self.fields['phone_number'].label = "رقم الجوال"
        self.fields['user_type'].label = "نوع المستخدم"
        self.fields['store_location'].label = "عنوان المتجر"
        self.fields['is_active'].label = "تفعيل المستخدم"
