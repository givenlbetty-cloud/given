from django.db import models
from django.conf import settings

class Programme(models.Model):
    CATEGORIES = (
        ('art_oratoire', 'Art Oratoire'),
        ('leadership', 'Leadership'),
        ('informatique', 'Informatique'),
        ('langues', 'Langues'),
        ('affaires', 'Affaires'),
    )
    # Mode Hybride
    TYPES = (
        ('online', 'En Ligne'),
        ('offline', 'Présentiel'),
        ('hybrid', 'Hybride'),
    )
    
    titre = models.CharField(max_length=200)
    categorie = models.CharField(max_length=20, choices=CATEGORIES, default='art_oratoire')
    type_formation = models.CharField(max_length=10, choices=TYPES, default='offline')
    description = models.TextField()
    image = models.ImageField(upload_to='programmes/', blank=True, null=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Pour les cours en ligne
    est_publie = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_categorie_display()} - {self.titre}"

class Chapitre(models.Model):
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name='chapitres')
    titre = models.CharField(max_length=200)
    ordre = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['ordre']

    def __str__(self):
        return self.titre

class Lecon(models.Model):
    chapitre = models.ForeignKey(Chapitre, on_delete=models.CASCADE, related_name='lecons')
    titre = models.CharField(max_length=200)
    contenu = models.TextField(help_text="Contenu HTML, Texte ou Embed Vidéo")
    video_url = models.URLField(blank=True, null=True, help_text="Lien YouTube/Vimeo")
    duree_minutes = models.IntegerField(default=10)
    ordre = models.IntegerField(default=0)
    est_gratuit = models.BooleanField(default=False, help_text="Accessible sans paiement (teaser)")

    class Meta:
        ordering = ['ordre']

    def __str__(self):
        return self.titre

class Session(models.Model):
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name='sessions')
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    lieu = models.CharField(max_length=200, default="Siège ATJ", blank=True)
    places_disponibles = models.IntegerField(default=20)
    
    # Pour le mode en ligne, on peut avoir une session "permanente" ou gérée différemment
    est_permanente = models.BooleanField(default=False, help_text="Pour les cours en ligne accessibles tout le temps")

    def __str__(self):
        date_str = "Permanent" if self.est_permanente else f"{self.date_debut}"
        return f"{self.programme.titre} ({date_str})"

class Inscription(models.Model):
    STATUT_PAIEMENT = (
        ('pending', 'En attente'),
        ('paid', 'Payé'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='inscriptions')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='inscriptions')
    date_inscription = models.DateTimeField(auto_now_add=True)
    statut_paiement = models.CharField(max_length=20, choices=STATUT_PAIEMENT, default='pending')
    statut_validation = models.BooleanField(default=False)
    progression = models.IntegerField(default=0, help_text="Pourcentage de progression (0-100)")

    def __str__(self):
        return f"{self.user} - {self.session}"

class Paiement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='paiements')
    inscription = models.ForeignKey(Inscription, on_delete=models.CASCADE, related_name='paiements')
    montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_paiement = models.DateTimeField(auto_now_add=True)
    valide = models.BooleanField(default=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Paiement {self.id} - {self.user.username} - {self.inscription.session.programme.titre}"
