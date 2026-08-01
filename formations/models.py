from django.db import models
from django.conf import settings


class Formation(models.Model):
    """Le contenu principal - ultra simple"""
    CATEGORIES = (
        ('art_oratoire', 'Art Oratoire'),
        ('leadership', 'Leadership'),
        ('informatique', 'Informatique'),
        ('langues', 'Langues'),
        ('affaires', 'Affaires'),
    )
    titre = models.CharField(max_length=200, verbose_name="Titre de la formation")
    categorie = models.CharField(max_length=20, choices=CATEGORIES, default='art_oratoire')
    description = models.TextField(verbose_name="Description")
    image_couverture = models.ImageField(upload_to='formations/', blank=True, null=True, verbose_name="Image de couverture")
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Prix (0 = gratuit)")
    conditions = models.TextField(blank=True, verbose_name="Pré-requis / Conditions")
    est_publie = models.BooleanField(default=False, verbose_name="Publier sur le site")

    class Meta:
        verbose_name = "Formation"
        verbose_name_plural = "Formations"
        ordering = ['categorie', 'titre']

    @property
    def est_gratuit(self):
        return self.prix == 0

    @property
    def nombre_lecons(self):
        return self.lecons.count()

    def __str__(self):
        return f"{self.get_categorie_display()} - {self.titre}"


class Lecon(models.Model):
    """Une leçon rattachée directement à la formation (plus de chapitre)"""
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name='lecons', verbose_name="Formation")
    titre = models.CharField(max_length=200, verbose_name="Titre de la leçon")
    ordre = models.IntegerField(default=0, verbose_name="Ordre")
    
    # Vidéo : upload direct OU lien YouTube
    video = models.FileField(upload_to='videos/', blank=True, null=True, verbose_name="Vidéo (MP4)", help_text="Uploader un fichier vidéo (prioritaire sur le lien)")
    video_url = models.URLField(blank=True, null=True, verbose_name="Ou lien YouTube/Vimeo", help_text="Lien vidéo externe (utilisé si aucun fichier uploadé)")
    
    contenu_texte = models.TextField(blank=True, verbose_name="Contenu texte", help_text="Texte, HTML ou description de la leçon")
    ressource_fichier = models.FileField(upload_to='ressources/', blank=True, null=True, verbose_name="Document (PDF, ZIP)", help_text="Support téléchargeable pour l'étudiant")
    
    duree_minutes = models.IntegerField(default=10, verbose_name="Durée (minutes)")
    est_gratuit = models.BooleanField(default=False, verbose_name="Accès gratuit (teaser)", help_text="Accessible sans paiement ni inscription")

    class Meta:
        verbose_name = "Leçon"
        verbose_name_plural = "Leçons"
        ordering = ['ordre']

    def get_video_embed_url(self):
        """Retourne l'URL embed YouTube/Vimeo si pas de fichier local"""
        if self.video:
            return self.video.url
        if not self.video_url:
            return None
        url = self.video_url
        if "youtube.com/watch?v=" in url:
            return url.replace("watch?v=", "embed/")
        elif "youtu.be/" in url:
            video_id = url.split("youtu.be/")[1].split("?")[0]
            return f"https://www.youtube.com/embed/{video_id}"
        elif "vimeo.com/" in url:
            video_id = url.split("vimeo.com/")[1].split("?")[0]
            return f"https://player.vimeo.com/video/{video_id}"
        return url

    @property
    def has_video(self):
        return bool(self.video or self.video_url)

    def __str__(self):
        return f"Leçon {self.ordre}: {self.titre}"


class Session(models.Model):
    """L'accès : en ligne (permanent) ou présentiel (dates + lieu)"""
    TYPE_SESSION = (
        ('en_ligne', '🌐 En Ligne'),
        ('presentiel', '📍 Présentiel'),
    )
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name='sessions', verbose_name="Formation")
    type_session = models.CharField(max_length=15, choices=TYPE_SESSION, default='en_ligne', verbose_name="Type")
    nom = models.CharField(max_length=200, default="Accès Libre", verbose_name="Nom de la session", help_text="Ex: 'Promo Octobre 2026' ou 'Accès Libre'")
    date_debut = models.DateField(null=True, blank=True, verbose_name="Date de début", help_text="Obligatoire si Présentiel")
    date_fin = models.DateField(null=True, blank=True, verbose_name="Date de fin")
    lieu = models.CharField(max_length=200, blank=True, default="Siège ATJ", verbose_name="Lieu", help_text="Pour le présentiel")
    places_disponibles = models.IntegerField(default=20, verbose_name="Places disponibles")

    class Meta:
        verbose_name = "Session"
        verbose_name_plural = "Sessions"
        ordering = ['-date_debut']

    def inscrit_count(self):
        return self.inscriptions.count()

    def places_restantes(self):
        return self.places_disponibles - self.inscrit_count()

    def is_open(self):
        from django.utils import timezone
        if self.places_restantes() <= 0:
            return False
        if self.type_session == 'en_ligne':
            return True
        today = timezone.now().date()
        if self.date_fin and today > self.date_fin:
            return False
        return True

    def __str__(self):
        return f"{self.formation.titre} - {self.nom}"


class Inscription(models.Model):
    STATUT_PAIEMENT = (
        ('pending', 'En attente'),
        ('paid', 'Payé'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='inscriptions')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='inscriptions', verbose_name="Session")
    date_inscription = models.DateTimeField(auto_now_add=True)
    statut_paiement = models.CharField(max_length=20, choices=STATUT_PAIEMENT, default='pending')
    statut_validation = models.BooleanField(default=False, verbose_name="Validée")
    progression = models.IntegerField(default=0, verbose_name="Progression (%)")
    completed_lessons = models.ManyToManyField(Lecon, blank=True, related_name='completed_by', verbose_name="Leçons complétées")

    class Meta:
        verbose_name = "Inscription"
        verbose_name_plural = "Inscriptions"

    def recalculate_progression(self):
        total = Lecon.objects.filter(formation=self.session.formation).count()
        completed = self.completed_lessons.count()
        self.progression = int((completed / total) * 100) if total > 0 else 0
        self.save(update_fields=['progression'])
        return self.progression

    def __str__(self):
        return f"{self.user.username} → {self.session}"


class Paiement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='paiements')
    inscription = models.ForeignKey(Inscription, on_delete=models.CASCADE, related_name='paiements')
    montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_paiement = models.DateTimeField(auto_now_add=True)
    valide = models.BooleanField(default=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"

    def __str__(self):
        return f"Paiement {self.id} - {self.user.username}"