from django import template

register = template.Library()

@register.filter
def whatsapp_number(phone):
    """
    تنسيق رقم الجوال لإضافته لرابط واتساب.
    يحذف المسافات والرموز مثل '+' و '-' ويضيف رمز الدولة إذا لم يكن موجود.
    """
    if not phone:
        return ''
    
    # إزالة الرموز والمسافات
    cleaned = ''.join(filter(str.isdigit, str(phone)))

    # تأكد من أن الرقم يبدأ بـ 966 أو أضفها (السعودية)
    if cleaned.startswith('0'):
        cleaned = '966' + cleaned[1:]
    elif not cleaned.startswith('966'):
        cleaned = '966' + cleaned

    return cleaned


@register.simple_tag
def order_status_badge(status):
    """
    عرض شارة الحالة بلون مخصص حسب حالة الطلب.
    """
    badges = {
        'pending': 'text-yellow-700 bg-yellow-100',
        'accepted': 'text-blue-700 bg-blue-100',
        'on_delivery': 'text-indigo-700 bg-indigo-100',
        'delivered': 'text-green-700 bg-green-100',
        'canceled': 'text-red-700 bg-red-100',
        'deleted': 'text-gray-500 bg-gray-100',
    }
    label = {
        'pending': 'قيد المراجعة',
        'accepted': 'تم القبول',
        'on_delivery': 'جاري التوصيل',
        'delivered': 'تم التسليم',
        'canceled': 'ملغي',
        'deleted': 'محذوف',
    }
    css_class = badges.get(status, 'text-gray-700 bg-gray-100')
    text = label.get(status, status)
    return f'<span class="px-2 py-1 rounded text-sm font-medium {css_class}">{text}</span>'
