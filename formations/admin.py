from django.contrib import admin
from django.utils.html import format_html
from .models import Formation, Lecon, Session, Inscription, Paiement


class LeconInline(admin.StackedInline):
    model = Lecon
    extra = 1
    fields = (
        ('titre', 'ordre'),
        ('video', 'video_url'),
        ('contenu_texte',),
        ('ressource_fichier',),
        ('duree_minutes', 'est_gratuit'),
    )
    ordering = ('ordre',)


class SessionInline(admin.StackedInline):
    model = Session
    extra = 1
    fields = (
        ('type_session', 'nom'),
        ('date_debut', 'date_fin'),
        ('lieu', 'places_disponibles'),
    )


@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie', 'prix_affiche', 'total_lecons', 'total_sessions', 'est_publie')
    list_filter = ('categorie', 'est_publie')
    search_fields = ('titre', 'description')
    inlines = [LeconInline, SessionInline]
    fieldsets = (
        ('📋 Informations', {
            'fields': ('titre', 'categorie', 'description', 'image_couverture')
        }),
        ('💰 Tarif & Conditions', {
            'fields': ('prix', 'conditions'),
        }),
        ('📢 Publication', {
            'fields': ('est_publie',),
        }),
    )

    def prix_affiche(self, obj):
        if obj.prix == 0:
            return format_html('<span style="color:green;font-weight:bold">GRATUIT</span>')
        return f"{obj.prix} €"
    prix_affiche.short_description = "Prix"

    def total_lecons(self, obj):
        return obj.nombre_lecons
    total_lecons.short_description = "Leçons"

    def total_sessions(self, obj):
        return obj.sessions.count()
    total_sessions.short_description = "Sessions"


@admin.register(Lecon)
class LeconAdmin(admin.ModelAdmin):
    list_display = ('titre', 'formation', 'ordre', 'has_video', 'est_gratuit')
    list_filter = ('formation', 'est_gratuit')
    search_fields = ('titre',)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('nom', 'formation', 'type_session', 'places_info', 'is_open')
    list_filter = ('type_session', 'formation')

    def places_info(self, obj):
        return f"{obj.inscrit_count()} / {obj.places_disponibles}"
    places_info.short_description = "Inscrits / Places"

    def is_open(self, obj):
        return obj.is_open()
    is_open.boolean = True
    is_open.short_description = "Ouverte"


@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'session', 'statut_paiement', 'progression_barre', 'statut_validation')
    list_filter = ('statut_paiement', 'statut_validation')
    actions = ['valider_inscriptions']

    def progression_barre(self, obj):
        return format_html(
            '<progress value="{}" max="100"></progress> {}%',
            obj.progression,
            obj.progression
        )
    progression_barre.short_description = "Progression"

    @admin.action(description='✅ Valider les inscriptions sélectionnées')
    def valider_inscriptions(self, request, queryset):
        queryset.update(statut_validation=True)


@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ('user', 'inscription', 'montant', 'valide', 'date_paiement')
    list_filter = ('valide',)