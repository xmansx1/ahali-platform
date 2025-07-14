from orders.models import Order
from stores.models import Store

def get_order_status_counts(user):
    try:
        store = Store.objects.get(user=user)
    except Store.DoesNotExist:
        return {
            'preparing': 0,
            'delivering': 0,
            'delivered': 0,
            'canceled': 0,
            'deleted': 0,
        }

    return {
        'preparing': Order.objects.filter(store=store, status='preparing').count(),
        'delivering': Order.objects.filter(store=store, status='delivering').count(),
        'delivered': Order.objects.filter(store=store, status='delivered').count(),
        'canceled': Order.objects.filter(store=store, status='canceled').count(),
        'deleted': Order.objects.filter(store=store, status='deleted').count(),
    }

def format_whatsapp_number(number):
    """
    يحول الرقم من 05xxxxxxxx أو +966xxxxxxxx إلى 966xxxxxxxx
    """
    if not number:
        return ""
    number = number.strip().replace(" ", "").replace("-", "")
    
    if number.startswith('05'):
        return '966' + number[1:]
    elif number.startswith('+966'):
        return number[1:]
    elif number.startswith('966'):
        return number
    return number
