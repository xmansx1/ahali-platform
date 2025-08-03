from .models import WelcomePopup
from datetime import datetime, timedelta

def active_welcome_popup(request):
    popup = WelcomePopup.objects.filter(is_active=True).order_by('-created_at').first()

    show_popup = False
    if popup:
        last_seen = request.COOKIES.get('last_welcome_popup')
        if last_seen:
            try:
                last_time = datetime.strptime(last_seen, "%Y-%m-%dT%H:%M:%S")
                if datetime.now() - last_time > timedelta(hours=5):
                    show_popup = True
            except Exception:
                show_popup = True  # في حال كان التاريخ غير صالح
        else:
            show_popup = True  # أول زيارة

    return {
        'welcome_popup': popup if show_popup else None
    }
