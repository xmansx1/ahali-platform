from django import template
from ads.models import PopupMessage
from datetime import datetime

register = template.Library()

@register.simple_tag
def popup_message():
    return PopupMessage.objects.filter(is_active=True).order_by('-created_at').first()
