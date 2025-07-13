from django import template
import re

register = template.Library()

@register.filter
def whatsapp_number(value):
    """
    يحول الرقم إلى تنسيق 966XXXXXXXXX لاستخدامه في روابط WhatsApp
    """
    if not value:
        return ''
    
    value = str(value).strip()

    # إزالة +966 أو 00966 أو 0 في البداية
    value = re.sub(r'^\+?0*966', '', value)
    value = re.sub(r'^0+', '', value)

    if value.startswith('5') and len(value) == 9:
        return '966' + value

    return value
