from django.contrib import admin
from .models import Programme, Session, Inscription, Chapitre, Lecon, Ressource

class RessourceInline(admin.TabularInline):
    model = Ressource
    extra = 1

class LeconInline(admin.StackedInline):
    model = Lecon
    extra = 1
    show_change_link = True  # Permet d'aller éditer la leçon en détail

class ChapitreInline(admin.StackedInline):
    model = Chapitre
    extra = 1
    show_change_link = True

class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie', 'type_formation', 'prix', 'est_publie')
    list_filter = ('categorie', 'type_formation', 'est_publie')
    search_fields = ('titre', 'description')
    inlines = [ChapitreInline]

class ChapitreAdmin(admin.ModelAdmin):
    list_display = ('titre', 'programme', 'ordre')
    list_filter = ('programme',)
    inlines = [LeconInline]

class LeconAdmin(admin.ModelAdmin):
    list_display = ('titre', 'chapitre', 'ordre', 'est_gratuit')
    list_filter = ('chapitre__programme',)
    search_fields = ('titre', 'contenu')
    inlines = [RessourceInline]
    fieldsets = (
        ('Détails de la Leçon', {
            'fields': ('chapitre', 'titre', 'ordre', 'est_gratuit')
        }),
        ('Contenu Multimédia', {
            'fields': ('video_url', 'contenu', 'duree_minutes'),
            'description': "Ajoutez ici l'URL de votre vidéo (YouTube/Vimeo) et le résumé détaillé."
        }),
    )

class InscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'session', 'statut_paiement', 'statut_validation')
    list_filter = ('statut_paiement', 'statut_validation')
    actions = ['valider_inscription']

    @admin.action(description='Valider les inscriptions sélectionnées')
    def valider_inscription(self, request, queryset):
        queryset.update(statut_validation=True)

admin.site.register(Programme, ProgrammeAdmin)
admin.site.register(Chapitre, ChapitreAdmin)
admin.site.register(Lecon, LeconAdmin)
admin.site.register(Session)
admin.site.register(Inscription, InscriptionAdmin)
