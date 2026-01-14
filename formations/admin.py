from django.contrib import admin
from .models import Programme, Session, Inscription

class InscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'session', 'statut_paiement', 'statut_validation')
    list_filter = ('statut_paiement', 'statut_validation')
    actions = ['valider_inscription']

    @admin.action(description='Valider les inscriptions sélectionnées')
    def valider_inscription(self, request, queryset):
        queryset.update(statut_validation=True)

admin.site.register(Programme)
admin.site.register(Session)
admin.site.register(Inscription, InscriptionAdmin)
