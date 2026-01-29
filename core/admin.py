from django.contrib import admin
from .models import SiteSettings, TeamMember

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'hero_title')
    fieldsets = (
        ('Identité du Site', {
            'fields': ('site_name', 'logo')
        }),
        ('Page d\'Accueil (Hero)', {
            'fields': ('hero_title', 'hero_subtitle', 'hero_image')
        }),
        ('Mission & Vision', {
            'fields': ('mission_title', 'mission_text')
        }),
        ('Page À Propos', {
            'fields': ('about_title', 'about_description')
        }),
        ('Contact & Pied de page', {
            'fields': ('contact_email', 'contact_phone', 'contact_address', 'footer_text')
        }),
    )
    
    def has_add_permission(self, request):
        # Allow adding only if no instance exists
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('nom', 'role', 'ordre')
    list_editable = ('ordre',)

