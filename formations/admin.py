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
    list_display = ('titre', 'categorie', 'get_type_display_pretty', 'get_prix_display', 'est_publie')
    list_filter = ('categorie', 'type_formation', 'est_publie')
    search_fields = ('titre', 'description')
    inlines = [ChapitreInline]
    fieldsets = (
        ('Informations Générales', {
            'fields': ('titre', 'categorie', 'type_formation', 'image')
        }),
        ('Conditions & Tarifs', {
            'fields': ('prix', 'conditions'),
            'description': "Mettez 0.00 pour une formation Gratuite."
        }),
        ('Description Détaillée', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
        ('Publication', {
            'fields': ('est_publie',),
            'description': "Cochez pour rendre visible sur le site."
        })
    )

    def get_inline_instances(self, request, obj=None):
        """
        Désactive l'ajout de Chapitres si la formation est en Présentiel.
        Les chapitres sont réservés aux formations en ligne ou hybrides.
        """
        inline_instances = super().get_inline_instances(request, obj)
        if obj and obj.type_formation == 'offline':
            return []
        return inline_instances

    def get_type_display_pretty(self, obj):
        return obj.get_type_formation_display()
    get_type_display_pretty.short_description = "Format"

    def get_prix_display(self, obj):
        if obj.prix == 0:
            return "GRATUIT"
        return f"{obj.prix} €"
    get_prix_display.short_description = "Tarif"


class SessionAdmin(admin.ModelAdmin):
    list_display = ('programme', 'get_date_range', 'lieu', 'places_restantes_info', 'is_open_registration')
    list_filter = ('programme', 'est_permanente', 'lieu')
    fieldsets = (
        ('Programme associé', {
             'fields': ('programme', 'est_permanente')
        }),
        ('Planification (Présentiel / Daté)', {
            'fields': ('date_debut', 'date_fin', 'date_limite_inscription'),
            'description': "Laissez vide si c'est une formation permanente en ligne."
        }),
        ('Logistique', {
            'fields': ('lieu', 'places_disponibles'),
            'description': "Lieu physique e capacité d'accueil."
        })
    )

    def get_date_range(self, obj):
        if obj.est_permanente:
            return "Permanent (Toujours ouvert)"
        if obj.date_debut and obj.date_fin:
            return f"{obj.date_debut.strftime('%d/%m/%Y')} - {obj.date_fin.strftime('%d/%m/%Y')}"
        return "Dates non définies"
    get_date_range.short_description = "Période"

    def places_restantes_info(self, obj):
        # Note: Ce calcul est approximatif sans requête count() directe, 
        # mais suffisant pour l'admin simple.
        taken = Inscription.objects.filter(session=obj).count()
        return f"{taken} / {obj.places_disponibles}"
    places_restantes_info.short_description = "Inscrits / Capacité"

    def is_open_registration(self, obj):
        from django.utils import timezone
        today = timezone.now().date()
        
        # Si permanent, toujours ouvert
        if obj.est_permanente:
            return True
            
        # Si date limite passée
        if obj.date_limite_inscription and today > obj.date_limite_inscription:
            return False
            
        # Si pas commencé ou en cours (si autorisé en cours)
        # Ici on suppose qu'on peut s'inscrire tant que date limit n'est pas passée
        return True
    is_open_registration.boolean = True
    is_open_registration.short_description = "Inscriptions Ouvertes"


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
            'fields': ('video_file', 'video_url', 'contenu', 'duree_minutes'),
            'description': "Chargez une vidéo locale OU mettez un lien YouTube. La vidéo locale est prioritaire."
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
admin.site.register(Session, SessionAdmin)
admin.site.register(Inscription, InscriptionAdmin)
