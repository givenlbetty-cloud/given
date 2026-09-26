from django.db import models
from accounts.models import CustomUser
from io import BytesIO
from django.core.files.base import ContentFile
import logging

logger = logging.getLogger(__name__)

# Optionnel — ne bloque jamais
try:
    from pdf2image import convert_from_bytes
except ImportError:
    convert_from_bytes = None


class Livre(models.Model):
    titre = models.CharField(max_length=200)
    auteur = models.CharField(max_length=200)
    CATEGORIES = [
        ('dev', 'Développement'),
        ('business', 'Business & Marketing'),
        ('design', 'Design & Art'),
        ('science', 'Science & Tech'),
        ('other', 'Autre'),
    ]
    categorie = models.CharField(max_length=20, choices=CATEGORIES, default='other')
    description = models.TextField()
    image = models.ImageField(upload_to='livres_images/', blank=True, null=True)
    fichier = models.FileField(upload_to='livres_fichiers/', help_text="PDF ou EPUB")
    prix = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, help_text="0.00 pour gratuit")
    date_creation = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            self.generate_cover_from_pdf()
        except Exception:
            # A failed thumbnail must not prevent a book from being imported.
            logger.exception("Could not generate a cover for book %s", self.pk)

    def generate_cover_from_pdf(self):
        """Create a first-page cover using the configured file storage."""
        if (
            not self.pk
            or not self.fichier
            or self.image
            or not convert_from_bytes
            or not self.fichier.name.lower().endswith('.pdf')
        ):
            return False

        self.fichier.open('rb')
        try:
            pdf_content = self.fichier.read()
        finally:
            self.fichier.close()

        if not pdf_content:
            return False

        pages = convert_from_bytes(
            pdf_content,
            first_page=1,
            last_page=1,
            size=(400, None),
        )
        if not pages:
            return False

        buffer = BytesIO()
        pages[0].convert('RGB').save(buffer, format='JPEG', quality=85)
        self.image.save(
            f'livre-{self.pk}-cover.jpg',
            ContentFile(buffer.getvalue()),
            save=False,
        )
        type(self).objects.filter(pk=self.pk).update(image=self.image.name)
        return True

    def is_free(self):
        return True

    def __str__(self):
        return self.titre


class AchatLivre(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    date_achat = models.DateTimeField(auto_now_add=True)
    derniere_page_lue = models.IntegerField(default=1)
    est_termine = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.livre.titre}"


class Note(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    contenu = models.TextField()
    page_reference = models.IntegerField(null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Note de {self.user.username} sur {self.livre.titre}"


class Avis(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE, related_name='avis')
    note = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    commentaire = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avis de {self.user.username} sur {self.livre.titre}"


class Favori(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favoris')
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE, related_name='favoris_users')
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'livre')

    def __str__(self):
        return f"{self.user.username} aime {self.livre.titre}"