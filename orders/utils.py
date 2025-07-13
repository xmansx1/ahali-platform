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
