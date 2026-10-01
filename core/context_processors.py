import re

from .models import SiteSettings

def site_settings(request):
    """Injecte la configuration du site dans tous les templates"""
    settings_obj = SiteSettings.objects.first()
    contact_phone = (settings_obj.contact_phone if settings_obj else '') or '+243 854 939 767'
    return {
        'site_settings': settings_obj,
        'site_contact_phone': contact_phone,
        'site_contact_phone_href': re.sub(r'[^\d+]', '', contact_phone),
        'site_whatsapp_number': re.sub(r'\D', '', contact_phone),
    }
