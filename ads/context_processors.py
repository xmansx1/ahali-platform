# ads/context_processors.py

from .models import WelcomePopup

def active_welcome_popup(request):
    popup = WelcomePopup.objects.filter(is_active=True).order_by('-created_at').first()
    return {'welcome_popup': popup}
