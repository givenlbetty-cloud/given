from .models import SiteSettings

def site_settings(request):
    """Injecte la configuration du site dans tous les templates"""
    settings_obj = SiteSettings.objects.first()
    return {'site_settings': settings_obj}
