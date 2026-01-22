from django.db import models

class SiteSettings(models.Model):
    """Configuration dynamique du site (Logo, Header, etc.)"""
    site_name = models.CharField(max_length=200, default="ATJ")
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    hero_image = models.ImageField(upload_to='site/', blank=True, null=True, help_text="Image de fond de la page d'accueil")
    hero_title = models.CharField(max_length=200, default="Révélez votre Potentiel")
    
    def save(self, *args, **kwargs):
        # Singleton pattern simple : on s'assure qu'il n'y a qu'une seule instance
        if not self.pk and SiteSettings.objects.exists():
            return SiteSettings.objects.first()
        return super().save(*args, **kwargs)

    def __str__(self):
        return "Configuration du Site"

    class Meta:
        verbose_name = "Configuration Site"
        verbose_name_plural = "Configuration Site"

class TeamMember(models.Model):
    """Membres de l'équipe / Staff"""
    nom = models.CharField(max_length=100)
    role = models.CharField(max_length=100, help_text="Ex: Directrice Académique, Mentor Python...")
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    ordre = models.IntegerField(default=0, help_text="Ordre d'affichage")
    linkedin = models.URLField(blank=True, null=True)
    
    class Meta:
        ordering = ['ordre']

    def __str__(self):
        return f"{self.nom} - {self.role}"

