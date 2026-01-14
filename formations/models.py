from django.db import models
from django.conf import settings

class Programme(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='programmes/', blank=True, null=True)

    def __str__(self):
        return self.titre

class Session(models.Model):
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name='sessions')
    date_debut = models.DateField()
    date_fin = models.DateField()
    places_disponibles = models.IntegerField(default=20)

    def __str__(self):
        return f"{self.programme.titre} ({self.date_debut})"

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
