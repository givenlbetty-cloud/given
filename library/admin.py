from django.contrib import admin
from .models import Livre, AchatLivre

@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'prix', 'is_free_display', 'date_creation')
    search_fields = ('titre', 'auteur')
    list_filter = ('date_creation', 'categorie')
    
    fieldsets = (
        ('Informations Générales', {
            'fields': ('titre', 'auteur', 'categorie', 'description')
        }),
        ('Fichiers & Images', {
            'fields': ('image', 'fichier')
        }),
        ('Tarification', {
            'fields': ('prix',),
            'description': 'Mettre le prix à 0.00 pour rendre le livre GRATUIT.'
        }),
    )

    def is_free_display(self, obj):
        return obj.is_free()
    is_free_display.boolean = True
    is_free_display.short_description = "Gratuit ?"

@admin.register(AchatLivre)
class AchatLivreAdmin(admin.ModelAdmin):
    list_display = ('user', 'livre', 'date_achat')
